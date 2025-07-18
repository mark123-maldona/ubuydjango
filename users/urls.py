from django.urls import path
from .views import (
    register, 
    get_all_sellers,
    edit_profile,
    change_password,
    user_settings,
    view_activity_history,
    account_management,
    profile_statistics,
    user_profile
)

urlpatterns = [
    path('register/', register, name='register'),
    path('sellers/', get_all_sellers, name='get_all_sellers'),
    
    # Profile Management URLs
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/view/<int:user_id>/', user_profile, name='user_profile'),
    path('profile/statistics/', profile_statistics, name='profile_statistics'),
    
    # Account Management URLs
    path('password/change/', change_password, name='change_password'),
    path('settings/', user_settings, name='user_settings'),
    path('activity/', view_activity_history, name='view_activity_history'),
    path('account/manage/', account_management, name='account_management'),
]
