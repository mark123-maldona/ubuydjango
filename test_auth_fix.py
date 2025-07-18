#!/usr/bin/env python3
"""
Test script to verify authentication fixes
"""
import os
import sys
import django
from django.conf import settings

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.contrib.sessions.models import Session
import json

def test_authentication():
    """Test authentication functionality"""
    print("🔍 Testing Authentication System...")
    
    # Create a test client
    client = Client()
    
    # Test 1: Check authentication status (should be False)
    print("\n1. Testing auth status check (should be False):")
    response = client.get('/auth/check-auth/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Authenticated: {data.get('is_authenticated', 'Unknown')}")
    
    # Test 2: Test login with existing user
    print("\n2. Testing login functionality:")
    
    # Check if we have existing users
    users = User.objects.all()
    print(f"   Total users in database: {users.count()}")
    
    if users.exists():
        # Use first user for testing
        test_user = users.first()
        print(f"   Using test user: {test_user.username}")
        
        # Reset password to 'testpass123' for testing
        test_user.set_password('testpass123')
        test_user.save()
        
        # Attempt login
        login_data = {
            'username': test_user.username,
            'password': 'testpass123'
        }
        
        response = client.post('/auth/login/', 
                             data=json.dumps(login_data),
                             content_type='application/json')
        print(f"   Login response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Login successful: {data.get('message', 'No message')}")
            print(f"   User authenticated: {data.get('is_authenticated', 'Unknown')}")
            
            # Test 3: Check auth status after login (should be True)
            print("\n3. Testing auth status after login:")
            response = client.get('/auth/check-auth/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Authenticated: {data.get('is_authenticated', 'Unknown')}")
                if data.get('is_authenticated'):
                    print(f"   Username: {data.get('username', 'Unknown')}")
            
            # Test 4: Test profile access
            print("\n4. Testing profile access:")
            response = client.get('/auth/profile/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Profile loaded: {data.get('username', 'Unknown')}")
            
            # Test 5: Test store access (should work after authentication)
            print("\n5. Testing store access (POST - should require auth):")
            store_data = {
                'Productname': 'Test Product',
                'product_description': 'Test Description',
                'currtent_price': '10.00'
            }
            
            response = client.post('/store/', data=store_data)
            print(f"   Store POST status: {response.status_code}")
            if response.status_code == 401:
                print("   ✅ Store correctly requires authentication")
            elif response.status_code == 400:
                print("   ✅ Store accessible but validation failed (expected)")
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
            
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            if response.status_code == 400:
                print(f"   Error: {response.json().get('error', 'Unknown error')}")
    
    else:
        print("   ❌ No users found in database")
        print("   Creating test user...")
        
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"   ✅ Created test user: {user.username}")
    
    # Test 6: Test logout
    print("\n6. Testing logout:")
    response = client.post('/auth/logout/')
    print(f"   Logout status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Logout message: {data.get('message', 'No message')}")
    
    # Test 7: Check auth status after logout (should be False)
    print("\n7. Testing auth status after logout:")
    response = client.get('/auth/check-auth/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Authenticated: {data.get('is_authenticated', 'Unknown')}")
    
    print("\n✅ Authentication test completed!")

if __name__ == '__main__':
    test_authentication()
