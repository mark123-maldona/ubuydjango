#!/usr/bin/env python
import os
import sys
import django
import json
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def quick_auth_test():
    """Quick test to verify authentication works"""
    
    print("⚡ QUICK AUTHENTICATION TEST")
    print("=" * 40)
    
    # Create test client
    client = Client()
    
    # Ensure test user exists
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('testpassword123')
        user.save()
        print("✅ Created test user")
    else:
        print("✅ Test user exists")
    
    # Test login
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    response = client.post(
        '/auth/login/',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"Login status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login successful")
        
        # Test auth check
        auth_response = client.get('/auth/check-auth/')
        print(f"Auth check status: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            data = auth_response.json()
            if data.get('is_authenticated'):
                print("✅ Authentication check passed")
                print(f"User: {data.get('username')}")
            else:
                print("❌ Authentication check failed")
        
        # Test profile
        profile_response = client.get('/auth/profile/')
        print(f"Profile status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            print("✅ Profile access successful")
        else:
            print("❌ Profile access failed")
    else:
        print("❌ Login failed")
        print(response.json())
    
    print("\n🎯 FRONTEND TESTING GUIDE:")
    print("=" * 40)
    print("1. Make sure Django server is running")
    print("2. Use credentials: testuser / testpassword123")
    print("3. Open browser dev tools")
    print("4. Check Network tab for Set-Cookie headers")
    print("5. Check Application > Cookies for sessionid")
    print("6. Clear cache if needed")

if __name__ == "__main__":
    quick_auth_test()
