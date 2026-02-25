// static/js/quiz.js
// Handles: Countdown Timer + Answer Lock + Lifeline UI Feedback

document.addEventListener('DOMContentLoaded', function () {

    /* ─────────────────────────────────────────
       TIMER CONFIGURATION
    ───────────────────────────────────────── */
    const TIMER_DURATION = 30;   // seconds per question
    const timerEl        = document.getElementById('timer-count');
    const timerCircle    = document.getElementById('timer-circle');
    const answerForm     = document.getElementById('answer-form');
    const optionBtns     = document.querySelectorAll('.option-btn:not(:disabled)');

    if (!timerEl || !answerForm) return;  // Not on play page

    let timeLeft  = TIMER_DURATION;
    let timerLock = false;   // Prevent double-submit

    /* ─────────────────────────────────────────
       TICK FUNCTION
    ───────────────────────────────────────── */
    function tick() {
        if (timerLock) return;

        timerEl.textContent = timeLeft;

        // Update visual state based on time remaining
        timerCircle.classList.remove('timer-warning', 'timer-danger');

        if (timeLeft <= 10 && timeLeft > 5) {
            timerCircle.classList.add('timer-warning');
        } else if (timeLeft <= 5) {
            timerCircle.classList.add('timer-danger');
        }

        if (timeLeft <= 0) {
            // Time's up — auto-submit a blank/invalid answer → triggers game over
            timeExpired();
            return;
        }

        timeLeft--;
    }

    /* ─────────────────────────────────────────
       TIME EXPIRED HANDLER
    ───────────────────────────────────────── */
    function timeExpired() {
        if (timerLock) return;
        timerLock = true;

        clearInterval(countdown);

        // Disable all buttons
        optionBtns.forEach(btn => {
            btn.disabled = true;
            btn.classList.add('eliminated');
        });

        timerEl.textContent = '0';
        timerCircle.classList.add('timer-danger');

        // Show overlay message
        showTimerOverlay();

        // Auto-submit with timeout answer after 1.5s
        setTimeout(function () {
            // Add hidden input to signal timeout
            const hidden = document.createElement('input');
            hidden.type  = 'hidden';
            hidden.name  = 'answer';
            hidden.value = 'TIMEOUT';
            answerForm.appendChild(hidden);
            answerForm.submit();
        }, 1500);
    }

    /* ─────────────────────────────────────────
       SHOW TIMEOUT OVERLAY
    ───────────────────────────────────────── */
    function showTimerOverlay() {
        const overlay = document.createElement('div');
        overlay.id    = 'timeout-overlay';
        overlay.innerHTML = `
            <div class="timeout-message">
                <i class="bi bi-clock-history"></i>
                <p>Time's Up!</p>
            </div>
        `;
        overlay.style.cssText = `
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease;
        `;
        overlay.querySelector('.timeout-message').style.cssText = `
            text-align: center;
            color: #f5c518;
            font-size: 2rem;
            font-weight: bold;
        `;
        document.body.appendChild(overlay);
    }

    /* ─────────────────────────────────────────
       LOCK BUTTONS ON CLICK (prevent double)
    ───────────────────────────────────────── */
    optionBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            if (timerLock) return;
            timerLock = true;
            clearInterval(countdown);

            // Visual feedback: highlight selected button
            btn.style.background    = 'linear-gradient(135deg, #1e3a5f, #2a4a7f)';
            btn.style.borderColor   = '#4a8fff';
            btn.style.color         = '#fff';

            // Disable all other buttons
            optionBtns.forEach(function (other) {
                if (other !== btn) {
                    other.disabled = true;
                    other.style.opacity = '0.4';
                }
            });
        });
    });

    /* ─────────────────────────────────────────
       START COUNTDOWN
    ───────────────────────────────────────── */
    tick(); // Run immediately
    const countdown = setInterval(tick, 1000);


    /* ─────────────────────────────────────────
       LIFELINE BUTTON CONFIRMATIONS
    ───────────────────────────────────────── */
    const lifelineForms = document.querySelectorAll('form[action*="lifeline"]');

    lifelineForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const actionUrl    = form.getAttribute('action');
            let confirmMessage = 'Use this lifeline?';

            if (actionUrl.includes('fifty_fifty')) {
                confirmMessage = '50:50 — Eliminate 2 wrong answers. Are you sure?';
            } else if (actionUrl.includes('skip')) {
                confirmMessage = 'Skip — Replace this question. Are you sure?';
            } else if (actionUrl.includes('audience_poll')) {
                confirmMessage = 'Audience Poll — See what the audience thinks. Are you sure?';
            }

            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        });
    });


    /* ─────────────────────────────────────────
       PRIZE LADDER SCROLL TO ACTIVE
    ───────────────────────────────────────── */
    const activeLevel = document.querySelector('.active-level');
    if (activeLevel) {
        setTimeout(function () {
            activeLevel.scrollIntoView({
                behavior: 'smooth',
                block:    'center'
            });
        }, 300);
    }


    /* ─────────────────────────────────────────
       KEYBOARD SHORTCUTS (A/B/C/D keys)
    ───────────────────────────────────────── */
    document.addEventListener('keydown', function (e) {
        if (timerLock) return;

        const key     = e.key.toUpperCase();
        const btnMap  = { A: 'A', B: 'B', C: 'C', D: 'D' };

        if (btnMap[key]) {
            const targetBtn = document.getElementById('btn-' + key);
            if (targetBtn && !targetBtn.disabled) {
                targetBtn.click();
            }
        }
    });

});
