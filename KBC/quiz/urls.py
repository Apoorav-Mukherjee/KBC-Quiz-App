# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [

    # ─────────────────────────────
    # Public Routes
    # ─────────────────────────────
    path(
        '',
        views.home_view,
        name='home'
    ),
    path(
        'leaderboard/',
        views.leaderboard_view,
        name='leaderboard'
    ),

    # ─────────────────────────────
    # Auth Routes
    # ─────────────────────────────
    path(
        'register/',
        views.register_view,
        name='register'
    ),
    path(
        'login/',
        views.login_view,
        name='login'
    ),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ─────────────────────────────
    # Dashboard
    # ─────────────────────────────
    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    # ─────────────────────────────
    # Game Routes
    # ─────────────────────────────
    path(
        'game/start/',
        views.start_game_view,
        name='start_game'
    ),
    path(
        'game/play/',
        views.play_view,
        name='play'
    ),
    path(
        'game/answer/',
        views.answer_view,
        name='answer'
    ),
    path(
        'game/quit/',
        views.quit_game_view,
        name='quit_game'
    ),
    path(
        'game/result/',
        views.result_view,
        name='result'
    ),

    # ─────────────────────────────
    # Lifeline Routes
    # ─────────────────────────────
    path(
        'game/lifeline/<str:lifeline_type>/',
        views.lifeline_view,
        name='lifeline'
    ),

]