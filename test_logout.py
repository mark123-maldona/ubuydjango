#!/usr/bin/env python
"""
Test logout functionality
"""
import requests
import json

def test_complete_auth_flow():
    """Test complete authentication flow: login -> check -> logout -> check"""
    print("=" * 60)
    print("TESTING COMPLETE AUTHENTICATION FLOW")
    print("=" * 60)
    
    # Base URLs
    base_url = "http://127.0.0.1:8000"
    login_url = f"{base_url}/auth/login/"
    logout_url = f"{base_url}/auth/logout/"
    check_auth_url = f"{base_url}/auth/check-auth/"
    
    # Test credentials
    credentials = {
        "username": "logintest",
        "password": "testpass123"
    }
    
    # Create session to maintain cookies
    session = requests.Session()
    
    try:
        # Step 1: Login
        print("1. Testing login...")
        login_response = session.post(
            login_url,
            json=credentials,
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:5173'
            }
        )
        
        print(f"   Login Status: {login_response.status_code}")
        print(f"   Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("   ✅ Login successful!")
            
            # Step 2: Check auth after login
            print("\\n2. Checking auth after login...")
            auth_response = session.get(
                check_auth_url,
                headers={'Origin': 'http://localhost:5173'}
            )
            
            print(f"   Auth Status: {auth_response.status_code}")
            print(f"   Auth Response: {auth_response.text}")
            
            auth_data = auth_response.json()
            if auth_data.get('is_authenticated'):
                print("   ✅ User is authenticated after login!")
                
                # Step 3: Logout
                print("\\n3. Testing logout...")
                
                # Get CSRF token from cookies
                csrf_token = session.cookies.get('csrftoken', '')
                print(f"   CSRF Token: {csrf_token}")
                
                logout_response = session.post(
                    logout_url,
                    headers={
                        'Origin': 'http://localhost:5173',
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json'
                    }
                )
                
                print(f"   Logout Status: {logout_response.status_code}")
                print(f"   Logout Response: {logout_response.text}")
                
                if logout_response.status_code == 200:
                    print("   ✅ Logout successful!")
                    
                    # Step 4: Check auth after logout
                    print("\\n4. Checking auth after logout...")
                    auth_after_logout = session.get(
                        check_auth_url,
                        headers={'Origin': 'http://localhost:5173'}
                    )
                    
                    print(f"   Auth Status: {auth_after_logout.status_code}")
                    print(f"   Auth Response: {auth_after_logout.text}")
                    
                    auth_data_after = auth_after_logout.json()
                    if not auth_data_after.get('is_authenticated'):
                        print("   ✅ User is NOT authenticated after logout!")
                        print("   🎉 Complete authentication flow works perfectly!")
                    else:
                        print("   ❌ User is still authenticated after logout!")
                        print("   🔧 Logout may not be clearing session properly")
                else:
                    print("   ❌ Logout failed!")
            else:
                print("   ❌ User is NOT authenticated after login!")
        else:
            print("   ❌ Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server!")
        print("   Make sure Django server is running: py manage.py runserver")
    except Exception as e:
        print(f"   ❌ Error during test: {e}")

if __name__ == "__main__":
    test_complete_auth_flow()
    
    print("\\n" + "=" * 60)
    print("AUTHENTICATION FLOW SUMMARY")
    print("=" * 60)
    print("This test verifies:")
    print("✅ Login with valid credentials")
    print("✅ Authentication check after login")
    print("✅ Logout functionality")
    print("✅ Authentication check after logout")
    print("")
    print("If all steps pass, your authentication system is working correctly!")
    print("If logout doesn't work, check:")
    print("1. Session clearing in logout view")
    print("2. Cookie deletion")
    print("3. Frontend session management")
