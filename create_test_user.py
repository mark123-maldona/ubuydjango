#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create a test user with known credentials"""
    
    print("👤 Creating test user for frontend authentication...")
    
    # Delete existing test user if any
    User.objects.filter(username='testuser').delete()
    
    # Create new test user
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123',
        first_name='Test',
        last_name='User'
    )
    
    print(f"✅ Created user: {test_user.username}")
    print(f"✅ Email: {test_user.email}")
    print(f"✅ Password: testpassword123")
    print(f"✅ User ID: {test_user.id}")
    
    # Verify user can be authenticated
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='testuser', password='testpassword123')
    
    if auth_user:
        print("✅ User authentication verified!")
        print("\n🎯 FRONTEND TESTING CREDENTIALS:")
        print("Username: testuser")
        print("Password: testpassword123")
        print("\nUse these credentials to test login in your React app!")
    else:
        print("❌ User authentication failed!")

if __name__ == "__main__":
    create_test_user()
