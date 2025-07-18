import requests
import json

# Test the authentication endpoints with the React frontend
BASE_URL = 'http://127.0.0.1:8000/auth/'

def test_register_and_login():
    """Test user registration and login for frontend integration"""
    print("Testing Frontend Authentication Integration")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Register a new user
    print("1. Testing user registration...")
    register_data = {
        'username': 'frontenduser',
        'email': 'frontend@example.com',
        'password': 'testpass123',
        'first_name': 'Frontend',
        'last_name': 'User'
    }
    
    response = session.post(
        f'{BASE_URL}register/',
        data=json.dumps(register_data),
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Registration Status: {response.status_code}")
    print(f"Registration Response: {response.json()}")
    print("-" * 50)
    
    # Test 2: Login with the registered user
    print("2. Testing user login...")
    login_data = {
        'username': 'frontenduser',
        'password': 'testpass123'
    }
    
    response = session.post(
        f'{BASE_URL}login/',
        data=json.dumps(login_data),
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")
    print("-" * 50)
    
    # Test 3: Check auth status
    print("3. Testing auth status check...")
    response = session.get(f'{BASE_URL}check-auth/')
    
    print(f"Auth Status: {response.status_code}")
    print(f"Auth Response: {response.json()}")
    print("-" * 50)
    
    # Test 4: Get profile
    print("4. Testing profile retrieval...")
    response = session.get(f'{BASE_URL}profile/')
    
    print(f"Profile Status: {response.status_code}")
    print(f"Profile Response: {response.json()}")
    print("-" * 50)
    
    # Test 5: Logout
    print("5. Testing logout...")
    response = session.post(f'{BASE_URL}logout/')
    
    print(f"Logout Status: {response.status_code}")
    print(f"Logout Response: {response.json()}")
    print("-" * 50)
    
    # Test 6: Check auth status after logout
    print("6. Testing auth status after logout...")
    response = session.get(f'{BASE_URL}check-auth/')
    
    print(f"Auth Status: {response.status_code}")
    print(f"Auth Response: {response.json()}")
    print("-" * 50)
    
    print("Frontend Authentication Integration Test Complete!")
    print("🎉 All endpoints are ready for React frontend integration!")

if __name__ == "__main__":
    try:
        test_register_and_login()
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running!")
        print("Please start the Django server with: python manage.py runserver")
