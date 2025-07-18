#!/usr/bin/env python
import os
import sys
import django
import json
import requests
from urllib.parse import urljoin

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User

def test_frontend_auth():
    """Test authentication as if it were coming from the frontend"""
    
    print("🔍 FRONTEND AUTHENTICATION DEBUG")
    print("=" * 60)
    
    # Use the actual URLs that the frontend would use
    BASE_URL = "http://127.0.0.1:8000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set headers to mimic frontend requests
    session.headers.update({
        'Origin': 'http://localhost:3000',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    
    print("\n1. 🌐 Testing initial authentication check...")
    try:
        response = session.get(f"{BASE_URL}/auth/check-auth/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {session.cookies}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. 🔑 Testing login with existing user...")
    # Try to login with an existing user
    try:
        # Get existing user
        user = User.objects.filter(username='testuser').first()
        if user:
            print(f"   Found user: {user.username}")
            
            # Test login
            login_data = {
                'username': 'testuser',
                'password': 'testpassword123'
            }
            
            response = session.post(
                f"{BASE_URL}/auth/login/", 
                data=json.dumps(login_data)
            )
            
            print(f"   Login Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            print(f"   Cookies after login: {session.cookies}")
            
            # Check if session cookie was set
            if 'sessionid' in session.cookies:
                print(f"   ✅ Session cookie set: {session.cookies['sessionid']}")
            else:
                print("   ❌ No session cookie set")
                
        else:
            print("   No existing user found, creating test user...")
            # Create a test user
            test_user = User.objects.create_user(
                username='frontendtest',
                email='frontend@test.com',
                password='testpassword123'
            )
            
            login_data = {
                'username': 'frontendtest',
                'password': 'testpassword123'
            }
            
            response = session.post(
                f"{BASE_URL}/auth/login/", 
                data=json.dumps(login_data)
            )
            
            print(f"   Login Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            print(f"   Cookies after login: {session.cookies}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. 🔐 Testing authentication check after login...")
    try:
        response = session.get(f"{BASE_URL}/auth/check-auth/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {session.cookies}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n4. 👤 Testing profile access...")
    try:
        response = session.get(f"{BASE_URL}/auth/profile/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 DEBUGGING RECOMMENDATIONS:")
    print("1. Check if your React app is sending cookies properly")
    print("2. Verify 'credentials: include' is in all fetch requests")
    print("3. Check browser developer tools for:")
    print("   - Network tab: Request/Response headers")
    print("   - Application tab: Cookies section")
    print("   - Console: CORS or authentication errors")
    print("4. Make sure both Django and React are running")
    print("5. Clear browser cache and cookies")

if __name__ == "__main__":
    test_frontend_auth()
