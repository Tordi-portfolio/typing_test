from django.db import models
from django.contrib.auth.models import User

class TypingTest(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    words = models.TextField()
    wpm = models.FloatField(default=0)
    accuracy = models.FloatField(default=0)
    errors = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"{self.user} - {self.difficulty} - WPM: {self.wpm}"
        return f"Anonymous - {self.difficulty} - WPM: {self.wpm}"