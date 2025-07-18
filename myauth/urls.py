from django.urls import path
from . import views
from . import enhanced_views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('check-auth/', views.check_auth_status, name='check_auth'),
    
    # Enhanced authentication endpoints
    path('enhanced-login/', enhanced_views.enhanced_login, name='enhanced_login'),
    path('enhanced-check-auth/', enhanced_views.enhanced_check_auth, name='enhanced_check_auth'),
    path('enhanced-profile/', enhanced_views.enhanced_profile, name='enhanced_profile'),
]
