from django.contrib import admin
from .models import User, Seller, UserSettings, ActivityHistory, UserStatistics

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'id']
    search_fields = ['username', 'email']
    list_filter = ['username']
    readonly_fields = ['id']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['Sellername', 'email', 'phone']
    search_fields = ['Sellername', 'email']
    list_filter = ['Sellername']

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'privacy_public_profile', 'created_at']
    list_filter = ['email_notifications', 'privacy_public_profile', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(ActivityHistory)
class ActivityHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp', 'ip_address']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'items_sold', 'items_bought', 'total_revenue', 'total_spent', 'profile_views']
    list_filter = ['last_updated']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']
