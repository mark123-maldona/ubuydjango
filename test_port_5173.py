#!/usr/bin/env python
import os
import sys
import django
import json
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User

def test_with_port_5173():
    """Test authentication with port 5173"""
    
    print("🔍 TESTING AUTHENTICATION WITH PORT 5173")
    print("=" * 60)
    
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
    
    # Create session to mimic browser behavior
    session = requests.Session()
    
    # Set headers to mimic Vite React app on port 5173
    session.headers.update({
        'Origin': 'http://localhost:5173',
        'Referer': 'http://localhost:5173/',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    BASE_URL = "http://127.0.0.1:8000"
    
    print("\n1. 🔍 Testing initial auth check...")
    try:
        response = session.get(f"{BASE_URL}/auth/check-auth/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. 🔑 Testing login...")
    try:
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        
        response = session.post(
            f"{BASE_URL}/auth/login/",
            data=json.dumps(login_data)
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {dict(session.cookies)}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. 🔍 Testing auth check after login...")
    try:
        response = session.get(f"{BASE_URL}/auth/check-auth/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n4. 👤 Testing profile access...")
    try:
        response = session.get(f"{BASE_URL}/auth/profile/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Clear browser cache and cookies")
    print("3. Try login with: testuser / testpassword123")
    print("4. Check browser dev tools for cookie issues")
    print("5. Make sure React app is on http://localhost:5173")

if __name__ == "__main__":
    test_with_port_5173()
