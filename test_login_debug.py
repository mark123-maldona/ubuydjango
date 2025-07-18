#!/usr/bin/env python
"""
Debug script to test login functionality
"""
import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_login_with_requests():
    """Test login using requests library (simulating frontend)"""
    print("=" * 50)
    print("TESTING LOGIN WITH REQUESTS (Frontend simulation)")
    print("=" * 50)
    
    # Test with a known user
    login_url = "http://127.0.0.1:8000/auth/login/"
    check_auth_url = "http://127.0.0.1:8000/auth/check-auth/"
    
    # Test user credentials
    test_credentials = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    # Create session to maintain cookies
    session = requests.Session()
    
    print(f"1. Testing login with credentials: {test_credentials['username']}")
    
    try:
        # Attempt login
        response = session.post(login_url, 
                              json=test_credentials,
                              headers={'Content-Type': 'application/json'})
        
        print(f"   Login response status: {response.status_code}")
        print(f"   Login response: {response.text}")
        print(f"   Login response cookies: {response.cookies}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            
            # Test auth check
            auth_response = session.get(check_auth_url)
            print(f"   Auth check response: {auth_response.text}")
            
        else:
            print("   ❌ Login failed!")
            
    except Exception as e:
        print(f"   ❌ Error during login test: {e}")

def test_login_with_django_client():
    """Test login using Django test client"""
    print("\n" + "=" * 50)
    print("TESTING LOGIN WITH DJANGO CLIENT")
    print("=" * 50)
    
    client = Client()
    
    # Test user credentials
    test_credentials = {
        "username": "frontenduser",
        "password": "testpass123"
    }
    
    print(f"1. Testing login with credentials: {test_credentials['username']}")
    
    try:
        # Attempt login
        response = client.post('/auth/login/', 
                             json.dumps(test_credentials),
                             content_type='application/json')
        
        print(f"   Login response status: {response.status_code}")
        print(f"   Login response: {response.content.decode()}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            
            # Test auth check
            auth_response = client.get('/auth/check-auth/')
            print(f"   Auth check response: {auth_response.content.decode()}")
            
        else:
            print("   ❌ Login failed!")
            
    except Exception as e:
        print(f"   ❌ Error during login test: {e}")

def check_user_credentials():
    """Check if test users exist and their passwords"""
    print("\n" + "=" * 50)
    print("CHECKING USER CREDENTIALS")
    print("=" * 50)
    
    test_users = ["testuser", "frontenduser", "maldona"]
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"User {username}: exists")
            print(f"  - ID: {user.id}")
            print(f"  - Email: {user.email}")
            print(f"  - Active: {user.is_active}")
            print(f"  - Last login: {user.last_login}")
            
            # Test password verification
            test_passwords = ["testpass123", "password123", "password", "123456"]
            for pwd in test_passwords:
                if user.check_password(pwd):
                    print(f"  - ✅ Password '{pwd}' works!")
                    break
            else:
                print(f"  - ❌ None of the test passwords work")
                
        except User.DoesNotExist:
            print(f"User {username}: does not exist")
        except Exception as e:
            print(f"Error checking user {username}: {e}")

if __name__ == "__main__":
    check_user_credentials()
    test_login_with_django_client()
    
    print("\n" + "=" * 50)
    print("NOTE: To test with requests, make sure Django server is running")
    print("Run: py manage.py runserver")
    print("Then uncomment the requests test below")
    print("=" * 50)
    
    # Uncomment to test with requests (requires server to be running)
    # test_login_with_requests()
