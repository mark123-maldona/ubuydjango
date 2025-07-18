#!/usr/bin/env python
"""
Test script to verify the authentication flow works properly
"""

import os
import sys
import django
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

def test_authentication_flow():
    """Test the complete authentication flow"""
    client = Client()
    
    # Test 1: Check auth status for unauthenticated user
    print("Test 1: Checking auth status for unauthenticated user...")
    response = client.get('/auth/check-auth/')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert data['is_authenticated'] == False, "Should not be authenticated"
    print("✓ Test 1 passed\n")
    
    # Test 2: Register a test user
    print("Test 2: Registering a test user...")
    test_user_data = {
        'username': 'testuser123',
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    response = client.post('/auth/register/', 
                          data=json.dumps(test_user_data),
                          content_type='application/json')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 201, f"Registration failed: {data}"
    print("✓ Test 2 passed\n")
    
    # Test 3: Login with the test user
    print("Test 3: Logging in with test user...")
    login_data = {
        'username': 'testuser123',
        'password': 'testpass123'
    }
    
    response = client.post('/auth/login/', 
                          data=json.dumps(login_data),
                          content_type='application/json')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200, f"Login failed: {data}"
    assert data['is_authenticated'] == True, "Should be authenticated after login"
    print("✓ Test 3 passed\n")
    
    # Test 4: Check auth status for authenticated user
    print("Test 4: Checking auth status for authenticated user...")
    response = client.get('/auth/check-auth/')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert data['is_authenticated'] == True, "Should be authenticated"
    assert data['username'] == 'testuser123', "Username should match"
    print("✓ Test 4 passed\n")
    
    # Test 5: Get user profile
    print("Test 5: Getting user profile...")
    response = client.get('/auth/profile/')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200, f"Profile fetch failed: {data}"
    assert data['username'] == 'testuser123', "Profile username should match"
    print("✓ Test 5 passed\n")
    
    # Test 6: Logout
    print("Test 6: Logging out...")
    response = client.post('/auth/logout/')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert response.status_code == 200, f"Logout failed: {data}"
    print("✓ Test 6 passed\n")
    
    # Test 7: Check auth status after logout
    print("Test 7: Checking auth status after logout...")
    response = client.get('/auth/check-auth/')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    assert data['is_authenticated'] == False, "Should not be authenticated after logout"
    print("✓ Test 7 passed\n")
    
    # Cleanup: Delete test user
    try:
        User.objects.get(username='testuser123').delete()
        print("✓ Test user cleaned up")
    except User.DoesNotExist:
        pass
    
    print("🎉 All authentication tests passed!")

if __name__ == '__main__':
    test_authentication_flow()
