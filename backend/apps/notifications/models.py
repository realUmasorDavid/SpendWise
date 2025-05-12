from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('BUDGET_ALERT', 'Budget Alert'),
        ('TRANSACTION', 'Transaction'),
        ('SYSTEM', 'System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"