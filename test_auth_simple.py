#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import json

def test_authentication():
    """Test authentication endpoints using Django test client"""
    
    print("Starting Django Authentication Tests...")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # Test 1: Register a new user
    print("1. Testing user registration...")
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    response = client.post(
        '/auth/register/',
        data=json.dumps(register_data),
        content_type='application/json'
    )
    
    print(f"Registration Status: {response.status_code}")
    print(f"Registration Response: {response.json()}")
    print("-" * 50)
    
    # Test 2: Login with the registered user
    print("2. Testing user login...")
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    response = client.post(
        '/auth/login/',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")
    print("-" * 50)
    
    # Test 3: Check authentication status
    print("3. Testing authentication status...")
    response = client.get('/auth/check-auth/')
    
    print(f"Auth Check Status: {response.status_code}")
    print(f"Auth Check Response: {response.json()}")
    print("-" * 50)
    
    # Test 4: Get user profile
    print("4. Testing user profile...")
    response = client.get('/auth/profile/')
    
    print(f"Profile Status: {response.status_code}")
    print(f"Profile Response: {response.json()}")
    print("-" * 50)
    
    # Test 5: Logout
    print("5. Testing user logout...")
    response = client.post('/auth/logout/')
    
    print(f"Logout Status: {response.status_code}")
    print(f"Logout Response: {response.json()}")
    print("-" * 50)
    
    # Test 6: Check authentication status after logout
    print("6. Testing authentication status after logout...")
    response = client.get('/auth/check-auth/')
    
    print(f"Auth Check Status: {response.status_code}")
    print(f"Auth Check Response: {response.json()}")
    print("-" * 50)
    
    # Test 7: Try to access profile after logout
    print("7. Testing profile access after logout...")
    response = client.get('/auth/profile/')
    
    print(f"Profile Status: {response.status_code}")
    print(f"Profile Response: {response.json()}")
    print("-" * 50)
    
    print("Authentication tests completed!")
    
    # Show created users
    print("\nUsers in database:")
    for user in User.objects.all():
        print(f"- {user.username} ({user.email})")

if __name__ == "__main__":
    test_authentication()
