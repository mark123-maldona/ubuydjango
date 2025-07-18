import requests
import json

# Base URL for the authentication endpoints
BASE_URL = 'http://127.0.0.1:8000/auth/'

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    response = requests.post(f'{BASE_URL}register/', 
                           data=json.dumps(user_data),
                           headers={'Content-Type': 'application/json'})
    
    print(f"Registration Status Code: {response.status_code}")
    print(f"Registration Response: {response.json()}")
    print("-" * 50)

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    response = requests.post(f'{BASE_URL}login/', 
                           data=json.dumps(login_data),
                           headers={'Content-Type': 'application/json'})
    
    print(f"Login Status Code: {response.status_code}")
    print(f"Login Response: {response.json()}")
    print("-" * 50)
    
    return response

def test_profile(session):
    """Test getting user profile"""
    print("Testing user profile...")
    
    response = session.get(f'{BASE_URL}profile/')
    
    print(f"Profile Status Code: {response.status_code}")
    print(f"Profile Response: {response.json()}")
    print("-" * 50)

def test_check_auth(session):
    """Test checking authentication status"""
    print("Testing authentication status...")
    
    response = session.get(f'{BASE_URL}check-auth/')
    
    print(f"Auth Check Status Code: {response.status_code}")
    print(f"Auth Check Response: {response.json()}")
    print("-" * 50)

def test_logout(session):
    """Test user logout"""
    print("Testing user logout...")
    
    response = session.post(f'{BASE_URL}logout/')
    
    print(f"Logout Status Code: {response.status_code}")
    print(f"Logout Response: {response.json()}")
    print("-" * 50)

def main():
    """Run all authentication tests"""
    print("Starting Authentication Tests...")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test registration
    test_register()
    
    # Test login
    login_response = test_login()
    
    # If login successful, test other endpoints
    if login_response.status_code == 200:
        # Update session with login cookies
        session.cookies.update(login_response.cookies)
        
        # Test profile
        test_profile(session)
        
        # Test auth check
        test_check_auth(session)
        
        # Test logout
        test_logout(session)
        
        # Test auth check after logout
        print("Testing auth status after logout...")
        test_check_auth(session)
    
    print("Authentication tests completed!")

if __name__ == "__main__":
    main()
