from django.db import models
from django.utils import timezone

# This model represents a user in the system.
# Users can have a username, email, password, and an optional profile picture.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

# Create your models here.

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    privacy_public_profile = models.BooleanField(default=True)
    privacy_show_email = models.BooleanField(default=False)
    privacy_show_activity = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Settings"

class ActivityHistory(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('product_view', 'Product View'),
        ('product_purchase', 'Product Purchase'),
        ('product_list', 'Product Listed'),
        ('profile_update', 'Profile Updated'),
        ('password_change', 'Password Changed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional activity data

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Activity Histories'

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} at {self.timestamp}"

class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    items_sold = models.PositiveIntegerField(default=0)
    items_bought = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    profile_views = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Statistics'

    def __str__(self):
        return f"{self.user.username}'s Statistics"

class Seller(models.Model):
    Sellername = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.Sellername
