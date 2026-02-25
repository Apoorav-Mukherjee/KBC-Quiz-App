# quiz/models.py

from django.db import models
from django.contrib.auth.models import User


# ----------------------------
# Difficulty Levels
# ----------------------------
DIFFICULTY_CHOICES = [
    ('easy',   'Easy'),
    ('medium', 'Medium'),
    ('hard',   'Hard'),
]


class Question(models.Model):
    """
    Represents a single MCQ question with 4 options.
    Each question belongs to a difficulty level (1–15).
    """
    text          = models.TextField()
    option_a      = models.CharField(max_length=255)
    option_b      = models.CharField(max_length=255)
    option_c      = models.CharField(max_length=255)
    option_d      = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')]
    )
    difficulty    = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    level         = models.PositiveIntegerField(
        help_text="Question level (1 to 15). Higher = harder."
    )

    def __str__(self):
        return f"[Level {self.level}] {self.text[:60]}"

    class Meta:
        ordering = ['level']


class GameSession(models.Model):
    """
    Stores each user's game attempt — current level, lifelines used,
    score achieved, and whether the session is still active.
    """
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('won',       'Won'),
        ('lost',      'Lost'),
        ('quit',      'Quit'),
    ]

    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    started_at        = models.DateTimeField(auto_now_add=True)
    ended_at          = models.DateTimeField(null=True, blank=True)

    current_level     = models.PositiveIntegerField(default=1)
    score             = models.PositiveIntegerField(default=0)
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Lifelines — each starts as available (True)
    lifeline_5050     = models.BooleanField(default=True)   # 50-50
    lifeline_skip     = models.BooleanField(default=True)   # Skip Question
    lifeline_poll     = models.BooleanField(default=True)   # Audience Poll

    # Track which question was served this turn (for lifeline logic)
    current_question  = models.ForeignKey(
        Question,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='sessions'
    )

    # Store eliminated options from 50-50 as comma-separated e.g. "B,C"
    eliminated_options = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | Level {self.current_level} | {self.status} | ₹{self.score}"

    class Meta:
        ordering = ['-score', '-started_at']

# quiz/models.py  ← append at bottom

# Prize ladder — Level : Prize Amount (₹)
PRIZE_LADDER = {
    1:  1000,
    2:  2000,
    3:  3000,
    4:  5000,
    5:  10000,
    6:  20000,
    7:  40000,
    8:  80000,
    9:  160000,
    10: 320000,
    11: 640000,
    12: 1250000,
    13: 2500000,
    14: 5000000,
    15: 10000000,
}

# Safe havens — player keeps this amount even if they lose after passing it
SAFE_HAVENS = {5: 10000, 10: 320000}