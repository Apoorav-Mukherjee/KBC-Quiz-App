# quiz/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Question, GameSession


# ----------------------------
# Question Admin
# ----------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin panel for managing quiz questions.
    Supports filtering, searching, and inline editing.
    """
    list_display  = ('level', 'difficulty', 'short_text', 'correct_option')
    list_filter   = ('difficulty', 'level')
    search_fields = ('text',)
    ordering      = ('level',)
    list_per_page = 20

    fieldsets = (
        ('Question', {
            'fields': ('text', 'level', 'difficulty')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d')
        }),
        ('Answer', {
            'fields': ('correct_option',)
        }),
    )

    def short_text(self, obj):
        """Display truncated question text in list view."""
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    short_text.short_description = 'Question'


# ----------------------------
# GameSession Admin
# ----------------------------
@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """
    Admin panel for viewing and managing game sessions.
    Read-only fields prevent accidental score tampering.
    """
    list_display  = (
        'user', 'current_level', 'score',
        'status', 'started_at', 'ended_at',
        'lifelines_remaining'
    )
    list_filter   = ('status',)
    search_fields = ('user__username',)
    ordering      = ('-score',)
    list_per_page = 20

    readonly_fields = (
        'user', 'started_at', 'ended_at',
        'current_level', 'score', 'status',
        'lifeline_5050', 'lifeline_skip', 'lifeline_poll',
        'current_question', 'eliminated_options'
    )

    fieldsets = (
        ('Player Info', {
            'fields': ('user', 'status', 'started_at', 'ended_at')
        }),
        ('Progress', {
            'fields': ('current_level', 'score', 'current_question')
        }),
        ('Lifelines', {
            'fields': ('lifeline_5050', 'lifeline_skip', 'lifeline_poll', 'eliminated_options')
        }),
    )

    def lifelines_remaining(self, obj):
        """Show count of lifelines still available."""
        count = sum([obj.lifeline_5050, obj.lifeline_skip, obj.lifeline_poll])
        return f"{count}/3"
    lifelines_remaining.short_description = 'Lifelines Left'

    def has_add_permission(self, request):
        """Prevent manual creation of game sessions from admin."""
        return False


# ----------------------------
# Extend Default User Admin
# ----------------------------
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Extended User admin showing extra info like
    total sessions and best score.
    """
    list_display = (
        'username', 'email', 'date_joined',
        'is_staff', 'total_sessions', 'best_score'
    )

    def total_sessions(self, obj):
        return obj.sessions.count()
    total_sessions.short_description = 'Total Games'

    def best_score(self, obj):
        best = obj.sessions.order_by('-score').first()
        return f"₹{best.score:,}" if best else "—"
    best_score.short_description = 'Best Score'


# ----------------------------
# Admin Site Customization
# ----------------------------
admin.site.site_header  = "Quiz Master Admin"
admin.site.site_title   = "Quiz Master"
admin.site.index_title  = "Welcome to Quiz Master Control Panel"