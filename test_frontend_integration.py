#!/usr/bin/env python
import os
import sys
import django
import json
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_frontend_integration():
    """Test frontend-backend integration for authentication"""
    
    print("🔗 Testing Frontend-Backend Integration")
    print("=" * 60)
    
    # Create a test client that mimics frontend behavior
    client = Client()
    
    # Clear any existing test users
    User.objects.filter(username='integrationtest').delete()
    
    print("\n1. 🌐 Testing CORS and session handling...")
    
    # Test 1: Check if check-auth endpoint works with proper headers
    print("   Testing /auth/check-auth/ endpoint...")
    response = client.get('/auth/check-auth/', HTTP_ORIGIN='http://localhost:3000')
    print(f"   ✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Response: {data}")
        print(f"   ✅ Is authenticated: {data.get('is_authenticated', False)}")
    
    # Test 2: Register a new user
    print("\n2. 📝 Testing registration with CORS headers...")
    register_data = {
        'username': 'integrationtest',
        'email': 'integration@test.com',
        'password': 'testpassword123',
        'first_name': 'Integration',
        'last_name': 'Test'
    }
    
    response = client.post(
        '/auth/register/',
        data=json.dumps(register_data),
        content_type='application/json',
        HTTP_ORIGIN='http://localhost:3000'
    )
    
    print(f"   ✅ Registration Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   ✅ User created: {result['username']}")
    else:
        print(f"   ❌ Registration failed: {response.content}")
    
    # Test 3: Login with the registered user
    print("\n3. 🔑 Testing login with session persistence...")
    login_data = {
        'username': 'integrationtest',
        'password': 'testpassword123'
    }
    
    response = client.post(
        '/auth/login/',
        data=json.dumps(login_data),
        content_type='application/json',
        HTTP_ORIGIN='http://localhost:3000'
    )
    
    print(f"   ✅ Login Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Login successful: {result['username']}")
        print(f"   ✅ Session key: {client.session.session_key}")
    else:
        print(f"   ❌ Login failed: {response.content}")
    
    # Test 4: Check authentication status after login
    print("\n4. 🔐 Testing auth status after login...")
    response = client.get('/auth/check-auth/', HTTP_ORIGIN='http://localhost:3000')
    
    print(f"   ✅ Auth Check Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Is authenticated: {result['is_authenticated']}")
        if result['is_authenticated']:
            print(f"   ✅ User ID: {result['user_id']}")
            print(f"   ✅ Username: {result['username']}")
    
    # Test 5: Get user profile
    print("\n5. 👤 Testing profile endpoint...")
    response = client.get('/auth/profile/', HTTP_ORIGIN='http://localhost:3000')
    
    print(f"   ✅ Profile Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Profile loaded: {result['username']}")
        print(f"   ✅ Email: {result['email']}")
    else:
        print(f"   ❌ Profile failed: {response.content}")
    
    # Test 6: Check cookies and session
    print("\n6. 🍪 Testing session and cookie handling...")
    print(f"   ✅ Session key: {client.session.session_key}")
    print(f"   ✅ Session items: {dict(client.session.items())}")
    
    # Test 7: Simulate a new request (like frontend would do)
    print("\n7. 🔄 Simulating fresh request (like frontend)...")
    
    # Create a new client but keep the same session
    new_client = Client()
    if client.session.session_key:
        new_client.session = client.session
    
    response = new_client.get('/auth/check-auth/', HTTP_ORIGIN='http://localhost:3000')
    print(f"   ✅ Fresh request status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Still authenticated: {result['is_authenticated']}")
    
    print("\n" + "=" * 60)
    print("🎉 FRONTEND INTEGRATION TEST COMPLETED!")
    
    # Instructions for frontend testing
    print("\n📋 FRONTEND TESTING INSTRUCTIONS:")
    print("1. Make sure Django server is running on http://127.0.0.1:8000")
    print("2. Start your React app on http://localhost:3000")
    print("3. Open browser dev tools and check Network tab")
    print("4. Try logging in with existing user: zesiro / (check database for password)")
    print("5. Check if cookies are being set and sent with requests")
    print("6. Look for CORS errors in console")
    
    print("\n🔍 DEBUGGING TIPS:")
    print("- Check if 'credentials: include' is in all fetch requests")
    print("- Verify CORS_ALLOW_CREDENTIALS = True in Django settings")
    print("- Ensure Django and React are running on correct ports")
    print("- Check browser cookies for sessionid")

if __name__ == "__main__":
    test_frontend_integration()
