from django.contrib import admin
from .models import TypingTest

@admin.register(TypingTest)
class TypingTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'wpm', 'accuracy', 'errors', 'time_taken', 'created_at')
    list_filter = ('created_at', 'accuracy', 'wpm')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)