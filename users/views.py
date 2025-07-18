from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import Http404
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Seller, UserSettings, ActivityHistory, UserStatistics
from .forms import (
    ProfileEditForm, 
    CustomPasswordChangeForm, 
    UserSettingsForm,
    AccountDeletionForm,
    DataExportForm
)
import json
import csv
import io
from datetime import datetime, timedelta

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            ActivityHistory.objects.create(
                user=user,
                activity_type='profile_update',
                description='User updated their profile information.',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Your profile has been updated!')
            return redirect('edit_profile')
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            ActivityHistory.objects.create(
                user=user,
                activity_type='password_change',
                description='User changed their password.',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('change_password')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def user_settings(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated!')
            return redirect('user_settings')
    else:
        form = UserSettingsForm(instance=user_settings)
    return render(request, 'users/user_settings.html', {'form': form})

@login_required
def view_activity_history(request):
    activities = ActivityHistory.objects.filter(user=request.user)
    paginator = Paginator(activities, 10)  # Show 10 activities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/activity_history.html', {'page_obj': page_obj})

@login_required
def account_management(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            form = AccountDeletionForm(request.POST)
            if form.is_valid():
                # Delete account logic here
                ActivityHistory.objects.create(
                    user=request.user,
                    activity_type='account_deletion',
                    description='User requested account deletion.',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                request.user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('home')  # Replace with your home page URL
        elif 'export_data' in request.POST:
            form = DataExportForm(request.POST)
            if form.is_valid():
                # Data export logic here
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="user_data.csv"'
                writer = csv.writer(response)
                selected_data_types = form.cleaned_data['data_types']
                if 'profile' in selected_data_types:
                    user_profile = [
                        ['ID', request.user.id],
                        ['Username', request.user.username],
                        ['Email', request.user.email],
                        ['Bio', request.user.bio],
                    ]
                    writer.writerows(user_profile)
                return response
            else:
                messages.error(request, 'There was an error with your request.')
    else:
        deletion_form = AccountDeletionForm()
        export_form = DataExportForm()
    return render(request, 'users/account_management.html', {
        'deletion_form': deletion_form,
        'export_form': export_form
    })

@login_required
def profile_statistics(request):
    user_stats, created = UserStatistics.objects.get_or_create(user=request.user)
    
    # Get recent activity stats
    recent_activities = ActivityHistory.objects.filter(
        user=request.user,
        timestamp__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    context = {
        'user_stats': user_stats,
        'recent_activities': recent_activities,
    }
    return render(request, 'users/profile_statistics.html', context)

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_settings = UserSettings.objects.filter(user=user).first()
    
    # Check if profile is public
    if user_settings and not user_settings.privacy_public_profile:
        if request.user != user:
            raise Http404("Profile is private")
    
    # Increment profile views if not viewing own profile
    if request.user != user and request.user.is_authenticated:
        user_stats, created = UserStatistics.objects.get_or_create(user=user)
        user_stats.profile_views += 1
        user_stats.save()
    
    # Get user statistics
    user_stats = UserStatistics.objects.filter(user=user).first()
    
    # Get recent activities if allowed
    activities = []
    if user_settings and user_settings.privacy_show_activity:
        activities = ActivityHistory.objects.filter(
            user=user,
            activity_type__in=['product_list', 'product_purchase']
        )[:10]
    
    context = {
        'profile_user': user,
        'user_stats': user_stats,
        'activities': activities,
        'user_settings': user_settings,
    }
    return render(request, 'users/user_profile.html', context)

def register(request):
    # Logic for user registration
    return HttpResponse("User registration page")
    # return render(request, 'users/register.html')

@api_view(['GET'])
def get_all_sellers(request):
    all_sellers = Seller.objects.all()
    sellers_data = []
    for seller in all_sellers:
        sellers_data.append({
            'id': seller.id,
            'Sellername': seller.Sellername,
            'email': seller.email,
            'phone': seller.phone,
        })
    return Response(sellers_data)
