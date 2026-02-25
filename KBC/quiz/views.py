# quiz/views.py

import random
from datetime import datetime

from django.shortcuts         import render, redirect, get_object_or_404
from django.contrib.auth      import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib           import messages
from django.utils             import timezone
from django.db.models         import Max

from .models  import Question, GameSession, PRIZE_LADDER, SAFE_HAVENS
from .forms   import RegisterForm, LoginForm


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_safe_score(level):
    """
    Return the safe haven score the player keeps
    even if they lose — based on levels crossed.
    """
    safe = 0
    for safe_level, amount in SAFE_HAVENS.items():
        if level > safe_level:
            safe = amount
    return safe


def get_active_session(user):
    """Return the user's currently active game session, or None."""
    return GameSession.objects.filter(user=user, status='active').first()


def get_question_for_level(level, exclude_ids=None):
    """
    Fetch a random question matching the given level.
    Optionally exclude already-seen question IDs.
    """
    qs = Question.objects.filter(level=level)
    if exclude_ids:
        qs = qs.exclude(id__in=exclude_ids)
    if not qs.exists():
        # Fallback: any question at this level
        qs = Question.objects.filter(level=level)
    if qs.exists():
        return random.choice(list(qs))
    return None


# ============================================================
# AUTH VIEWS
# ============================================================

# In quiz/views.py — replace home_view with this

def home_view(request):
    """Public landing page with prize ladder preview."""
    prize_ladder_preview = list(PRIZE_LADDER.items())  # [(1,1000), (2,2000)...]
    return render(request, 'home.html', {
        'prize_ladder_preview': prize_ladder_preview
    })


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Your account is ready.")
        return redirect('dashboard')

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect('dashboard')

    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """Log out the current user."""
    # If there's an active session, mark it as quit
    session = get_active_session(request.user)
    if session:
        session.status   = 'quit'
        session.ended_at = timezone.now()
        session.score    = get_safe_score(session.current_level)
        session.save()

    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard_view(request):
    """
    User dashboard showing:
    - Play button
    - Past game sessions
    - Personal best score
    """
    sessions = GameSession.objects.filter(
        user=request.user
    ).exclude(status='active').order_by('-started_at')[:5]

    best = GameSession.objects.filter(
        user=request.user
    ).aggregate(best=Max('score'))['best'] or 0

    active_session = get_active_session(request.user)

    context = {
        'sessions':       sessions,
        'best_score':     best,
        'active_session': active_session,
        'prize_ladder':   PRIZE_LADDER,
    }
    return render(request, 'quiz/dashboard.html', context)


# ============================================================
# GAME VIEWS
# ============================================================

@login_required
def start_game_view(request):
    """
    Start a new game session.
    Ends any existing active session first.
    """
    # Close any lingering active session
    old = get_active_session(request.user)
    if old:
        old.status   = 'quit'
        old.ended_at = timezone.now()
        old.save()

    # Pick a question for level 1
    question = get_question_for_level(1)
    if not question:
        messages.error(request, "No questions found. Please contact admin.")
        return redirect('dashboard')

    # Create new session
    session = GameSession.objects.create(
        user             = request.user,
        current_level    = 1,
        current_question = question,
        score            = 0,
    )

    return redirect('play')


@login_required
def play_view(request):
    session = get_active_session(request.user)
    if not session:
        messages.warning(request, "No active game. Start a new one!")
        return redirect('dashboard')

    question = session.current_question
    if not question:
        messages.error(request, "Question not found. Please restart.")
        return redirect('dashboard')

    eliminated = session.eliminated_options.split(',') if session.eliminated_options else []

    # Retrieve audience poll from Django session if available
    audience_poll = request.session.pop('audience_poll', None)

    # Label map for template iteration
    option_labels = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}

    context = {
        'session':        session,
        'question':       question,
        'eliminated':     eliminated,
        'prize_ladder':   PRIZE_LADDER,
        'safe_havens':    SAFE_HAVENS,
        'current_prize':  PRIZE_LADDER.get(session.current_level, 0),
        'option_labels':  option_labels,
        'audience_poll':  audience_poll,
    }
    return render(request, 'quiz/play.html', context)

@login_required
def answer_view(request):
    """
    Process the player's answer.
    - Correct  → advance to next level or win
    - Wrong    → game over, apply safe haven score
    """
    if request.method != 'POST':
        return redirect('play')

    session = get_active_session(request.user)
    if not session:
        return redirect('dashboard')
    
    chosen = request.POST.get('answer', '').upper()
    question = session.current_question

    # Handle timer timeout — treat as wrong answer
    if chosen == 'TIMEOUT':
        safe_score       = get_safe_score(session.current_level)
        session.status   = 'lost'
        session.score    = safe_score
        session.ended_at = timezone.now()
        session.save()
        return redirect('result')

    if not question or chosen not in ['A', 'B', 'C', 'D']:
        messages.error(request, "Invalid answer. Please try again.")
        return redirect('play')
    
    # ── CORRECT ANSWER ──
    if chosen == question.correct_option:
        current_level = session.current_level
        prize         = PRIZE_LADDER.get(current_level, 0)

        # Player wins the game at level 15
        if current_level == 15:
            session.status   = 'won'
            session.score    = prize
            session.ended_at = timezone.now()
            session.save()
            return redirect('result')

        # Advance to next level
        next_level = current_level + 1
        next_q     = get_question_for_level(next_level)

        if not next_q:
            messages.error(request, f"No question found for level {next_level}. Contact admin.")
            return redirect('play')

        session.current_level     = next_level
        session.score             = prize
        session.current_question  = next_q
        session.eliminated_options = ''   # Reset 50-50 for new question
        session.save()
        return redirect('play')

    # ── WRONG ANSWER ──
    else:
        safe_score       = get_safe_score(session.current_level)
        session.status   = 'lost'
        session.score    = safe_score
        session.ended_at = timezone.now()
        session.save()
        return redirect('result')


@login_required
def quit_game_view(request):
    """
    Player voluntarily quits.
    They keep their current safe haven amount.
    """
    session = get_active_session(request.user)
    if session:
        session.status   = 'quit'
        session.score    = get_safe_score(session.current_level)
        session.ended_at = timezone.now()
        session.save()
    return redirect('result')


# ============================================================
# LIFELINE VIEWS
# ============================================================

@login_required
def lifeline_view(request, lifeline_type):
    """
    Handle all three lifelines:
    - fifty_fifty  : eliminate 2 wrong options
    - skip         : replace current question
    - audience_poll: return simulated poll percentages
    """
    session = get_active_session(request.user)
    if not session or request.method != 'POST':
        return redirect('play')

    question = session.current_question

    # ── 50-50 ──
    if lifeline_type == 'fifty_fifty' and session.lifeline_5050:
        wrong_options = [
            opt for opt in ['A', 'B', 'C', 'D']
            if opt != question.correct_option
        ]
        eliminated = random.sample(wrong_options, 2)
        session.lifeline_5050        = False
        session.eliminated_options   = ','.join(eliminated)
        session.save()

    # ── SKIP ──
    elif lifeline_type == 'skip' and session.lifeline_skip:
        new_q = get_question_for_level(
            session.current_level,
            exclude_ids=[question.id]
        )
        if new_q:
            session.current_question   = new_q
            session.eliminated_options = ''
        session.lifeline_skip = False
        session.save()

    # ── AUDIENCE POLL ──
    elif lifeline_type == 'audience_poll' and session.lifeline_poll:
        correct = question.correct_option
        # Give correct answer a higher probability
        correct_pct = random.randint(45, 75)
        remaining   = 100 - correct_pct
        others      = [o for o in ['A', 'B', 'C', 'D'] if o != correct]

        # Split remaining % among wrong options
        split1 = random.randint(0, remaining)
        split2 = random.randint(0, remaining - split1)
        split3 = remaining - split1 - split2

        splits = [split1, split2, split3]
        random.shuffle(splits)

        poll = {}
        for i, opt in enumerate(others):
            poll[opt] = splits[i]
        poll[correct] = correct_pct

        session.lifeline_poll = False
        session.save()

        # Pass poll data back to play view via session
        request.session['audience_poll'] = poll

    return redirect('play')


# ============================================================
# RESULT VIEW
# ============================================================

@login_required
def result_view(request):
    """
    Show game result — win, loss, or quit.
    Displays final score and message.
    """
    # Get the most recent completed session
    session = GameSession.objects.filter(
        user=request.user
    ).exclude(status='active').order_by('-ended_at').first()

    if not session:
        return redirect('dashboard')

    context = {
        'session':      session,
        'prize_ladder': PRIZE_LADDER,
    }
    return render(request, 'quiz/result.html', context)


# ============================================================
# LEADERBOARD VIEW
# ============================================================

def leaderboard_view(request):
    """
    Public leaderboard — top 10 scores across all users.
    One entry per user (their personal best).
    """
    # Get best score per user
    from django.db.models import Max
    top_sessions = (
        GameSession.objects
        .exclude(status='active')
        .values('user__username')
        .annotate(best_score=Max('score'))
        .order_by('-best_score')[:10]
    )

    context = {
        'top_sessions': top_sessions,
    }
    return render(request, 'quiz/leaderboard.html', context)