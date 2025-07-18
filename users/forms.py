from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User, UserSettings
import re

class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username is already taken by another user
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError("This username is already taken.")
            
            # Username validation
            if len(username) < 3:
                raise ValidationError("Username must be at least 3 characters long.")
            
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already taken by another user
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("This email is already registered.")
        
        return email
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (max 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError("Avatar file size must be less than 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if avatar.content_type not in allowed_types:
                raise ValidationError("Avatar must be a JPEG, PNG, GIF, or WebP image.")
        
        return avatar

class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with better styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            # Custom password validation
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            
            if not re.search(r'[A-Za-z]', password):
                raise ValidationError("Password must contain at least one letter.")
            
            if not re.search(r'[0-9]', password):
                raise ValidationError("Password must contain at least one number.")
        
        return password

class UserSettingsForm(forms.ModelForm):
    """Form for user settings and preferences"""
    
    class Meta:
        model = UserSettings
        fields = [
            'email_notifications',
            'sms_notifications',
            'marketing_emails',
            'privacy_public_profile',
            'privacy_show_email',
            'privacy_show_activity'
        ]
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marketing_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_public_profile': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_show_activity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'email_notifications': 'Email Notifications',
            'sms_notifications': 'SMS Notifications',
            'marketing_emails': 'Marketing Emails',
            'privacy_public_profile': 'Make Profile Public',
            'privacy_show_email': 'Show Email on Profile',
            'privacy_show_activity': 'Show Activity History',
        }
        help_texts = {
            'email_notifications': 'Receive email notifications for account activities',
            'sms_notifications': 'Receive SMS notifications for important updates',
            'marketing_emails': 'Receive marketing emails and promotional offers',
            'privacy_public_profile': 'Allow others to view your profile',
            'privacy_show_email': 'Display your email address on your public profile',
            'privacy_show_activity': 'Show your activity history on your profile',
        }

class AccountDeletionForm(forms.Form):
    """Form for account deletion confirmation"""
    
    confirmation = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type "DELETE" to confirm'
        }),
        help_text='Type "DELETE" to confirm account deletion'
    )
    
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Please tell us why you are deleting your account (optional)',
            'rows': 3
        }),
        required=False,
        help_text='Optional: Help us improve by telling us why you are leaving'
    )
    
    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if confirmation != 'DELETE':
            raise ValidationError('Please type "DELETE" to confirm account deletion.')
        return confirmation

class DataExportForm(forms.Form):
    """Form for data export options"""
    
    EXPORT_FORMATS = [
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ]
    
    DATA_TYPES = [
        ('profile', 'Profile Information'),
        ('activities', 'Activity History'),
        ('statistics', 'Account Statistics'),
        ('settings', 'Account Settings'),
    ]
    
    export_format = forms.ChoiceField(
        choices=EXPORT_FORMATS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='json'
    )
    
    data_types = forms.MultipleChoiceField(
        choices=DATA_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        initial=['profile', 'activities', 'statistics', 'settings']
    )
