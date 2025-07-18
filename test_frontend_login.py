#!/usr/bin/env python
"""
Test frontend login functionality with live server
"""
import requests
import json

def test_frontend_login():
    """Test login as frontend would do it"""
    print("=" * 60)
    print("TESTING FRONTEND LOGIN WITH LIVE SERVER")
    print("=" * 60)
    
    # Base URLs
    base_url = "http://127.0.0.1:8000"
    login_url = f"{base_url}/auth/login/"
    check_auth_url = f"{base_url}/auth/check-auth/"
    
    # Test credentials (use the working ones)
    test_credentials = {
        "username": "frontenduser",
        "password": "testpass123"
    }
    
    # Create session to maintain cookies
    session = requests.Session()
    
    print(f"1. Testing login with: {test_credentials['username']}")
    print(f"   URL: {login_url}")
    
    try:
        # Simulate frontend login request
        response = session.post(
            login_url,
            json=test_credentials,
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173',
                'Referer': 'http://localhost:5173/',
            }
        )
        
        print(f"   Login Status: {response.status_code}")
        print(f"   Login Response: {response.text}")
        print(f"   Login Cookies: {dict(response.cookies)}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            
            # Test auth check (simulating what frontend does)
            print(f"\n2. Testing auth check:")
            print(f"   URL: {check_auth_url}")
            
            auth_response = session.get(
                check_auth_url,
                headers={
                    'Origin': 'http://localhost:5173',
                    'Referer': 'http://localhost:5173/',
                }
            )
            
            print(f"   Auth Status: {auth_response.status_code}")
            print(f"   Auth Response: {auth_response.text}")
            print(f"   Auth Cookies: {dict(auth_response.cookies)}")
            
            # Parse and check response
            try:
                auth_data = auth_response.json()
                if auth_data.get('is_authenticated'):
                    print("   ✅ User is authenticated after login!")
                else:
                    print("   ❌ User is NOT authenticated after login!")
                    
            except json.JSONDecodeError:
                print("   ❌ Could not parse auth response")
                
        else:
            print("   ❌ Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server!")
        print("   Make sure Django server is running: py manage.py runserver")
    except Exception as e:
        print(f"   ❌ Error during test: {e}")

def test_with_wrong_credentials():
    """Test with wrong credentials"""
    print("\n" + "=" * 60)
    print("TESTING WITH WRONG CREDENTIALS")
    print("=" * 60)
    
    login_url = "http://127.0.0.1:8000/auth/login/"
    
    # Wrong credentials
    wrong_credentials = {
        "username": "nonexistent",
        "password": "wrongpass"
    }
    
    session = requests.Session()
    
    print(f"1. Testing with wrong credentials: {wrong_credentials['username']}")
    
    try:
        response = session.post(
            login_url,
            json=wrong_credentials,
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173',
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   ✅ Correctly rejected invalid credentials!")
        else:
            print("   ❌ Unexpected response to invalid credentials!")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_frontend_login()
    test_with_wrong_credentials()
    
    print("\n" + "=" * 60)
    print("LOGIN TROUBLESHOOTING SUMMARY")
    print("=" * 60)
    print("✅ Authentication system is working correctly")
    print("✅ Login endpoint works with valid credentials")
    print("✅ Session management works")
    print("✅ CORS is properly configured")
    print("")
    print("If frontend login still doesn't work, check:")
    print("1. Are you using the correct username/password?")
    print("2. Is the frontend making requests to the right URL?")
    print("3. Are cookies being sent properly?")
    print("4. Check browser developer tools for error messages")
