#!/usr/bin/env python3
"""
Test script to verify enhanced authentication system
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

def test_enhanced_authentication():
    """Test enhanced authentication functionality"""
    print("🚀 Testing Enhanced Authentication System...")
    
    # Create a test client
    client = Client()
    
    # Get a user to test with
    user = User.objects.get(username='penuel')
    print(f"Testing with user: {user.username}")
    
    # Test 1: Enhanced login
    print("\n1. Testing enhanced login:")
    login_data = {
        'username': user.username,
        'password': 'testpass123'  # We'll set this password
    }
    
    # Set password for testing
    user.set_password('testpass123')
    user.save()
    
    response = client.post('/auth/enhanced-login/', 
                         data=json.dumps(login_data),
                         content_type='application/json')
    print(f"   Enhanced login status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Login successful: {data.get('message')}")
        print(f"   Session key: {data.get('session_key')}")
        
        # Test 2: Enhanced check auth
        print("\n2. Testing enhanced check auth:")
        response = client.get('/auth/enhanced-check-auth/')
        print(f"   Enhanced check auth status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ User authenticated: {data.get('is_authenticated')}")
            print(f"   Username: {data.get('username')}")
            
            # Test 3: Enhanced profile
            print("\n3. Testing enhanced profile:")
            response = client.get('/auth/enhanced-profile/')
            print(f"   Enhanced profile status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Profile loaded: {data.get('username')}")
                print(f"   Email: {data.get('email')}")
                
                # Test 4: Test store access (should work with session)
                print("\n4. Testing store access with session:")
                store_data = {
                    'Productname': 'Test Product Enhanced',
                    'product_description': 'Test Description Enhanced',
                    'currtent_price': '25.00'
                }
                
                response = client.post('/store/', data=store_data)
                print(f"   Store POST status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Store access successful with authentication")
                elif response.status_code == 400:
                    print("   ✅ Store accessible but validation failed (expected)")
                elif response.status_code == 401:
                    print("   ❌ Store still requires authentication - middleware issue")
                else:
                    print(f"   ❓ Unexpected response: {response.status_code}")
                
            else:
                print(f"   ❌ Profile failed: {response.status_code}")
        else:
            print(f"   ❌ Enhanced check auth failed: {response.status_code}")
    else:
        print(f"   ❌ Enhanced login failed: {response.status_code}")
        if response.status_code == 400:
            print(f"   Error: {response.json()}")

    # Test 5: Test with specific session cookie
    print("\n5. Testing with specific session cookie:")
    
    # Create a new client and manually set the session cookie
    client2 = Client()
    client2.cookies['sessionid'] = '5z8gf9wq03x04w1xxlkfxg417s060tke'
    
    # Test enhanced check auth with the cookie
    response = client2.get('/auth/enhanced-check-auth/')
    print(f"   Enhanced check auth with cookie: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ User authenticated: {data.get('is_authenticated')}")
        if data.get('is_authenticated'):
            print(f"   Username: {data.get('username')}")
        else:
            print("   ❌ User not authenticated despite valid session")
            print(f"   Session key: {data.get('session_key')}")
            print(f"   Cookie session: {data.get('cookie_session')}")
    
    # Test 6: Test enhanced profile with cookie
    print("\n6. Testing enhanced profile with cookie:")
    response = client2.get('/auth/enhanced-profile/')
    print(f"   Enhanced profile with cookie: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Profile loaded: {data.get('username')}")
    else:
        print(f"   ❌ Profile failed: {response.status_code}")
    
    print("\n✅ Enhanced authentication test completed!")

if __name__ == '__main__':
    test_enhanced_authentication()
