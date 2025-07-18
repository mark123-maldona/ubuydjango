#!/usr/bin/env python
"""
Reset user passwords for testing
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User

def reset_passwords():
    """Reset passwords for test users"""
    print("=" * 50)
    print("RESETTING USER PASSWORDS")
    print("=" * 50)
    
    # Users to reset
    users_to_reset = [
        {"username": "testuser", "password": "testpass123"},
        {"username": "frontenduser", "password": "testpass123"}, 
        {"username": "maldona", "password": "testpass123"}
    ]
    
    for user_data in users_to_reset:
        username = user_data["username"]
        password = user_data["password"]
        
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            
            # Verify password works
            if user.check_password(password):
                print(f"✅ {username}: Password reset successfully")
            else:
                print(f"❌ {username}: Password reset failed")
                
        except User.DoesNotExist:
            print(f"❌ {username}: User does not exist")
        except Exception as e:
            print(f"❌ {username}: Error - {e}")

def create_test_user():
    """Create a new test user if needed"""
    print("\n" + "=" * 50)
    print("CREATING TEST USER")
    print("=" * 50)
    
    username = "logintest"
    password = "testpass123"
    email = "logintest@example.com"
    
    try:
        # Check if user exists
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists")
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✅ Password reset for {username}")
        else:
            # Create new user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name="Login",
                last_name="Test"
            )
            print(f"✅ Created new user: {username}")
            
        # Verify
        if user.check_password(password):
            print(f"✅ Login test user is ready!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Email: {email}")
        else:
            print(f"❌ Password verification failed")
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")

if __name__ == "__main__":
    reset_passwords()
    create_test_user()
    
    print("\n" + "=" * 50)
    print("TESTING CREDENTIALS")
    print("=" * 50)
    
    # Test all users
    test_users = ["testuser", "frontenduser", "maldona", "logintest"]
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            if user.check_password("testpass123"):
                print(f"✅ {username}: testpass123 works")
            else:
                print(f"❌ {username}: testpass123 does NOT work")
        except User.DoesNotExist:
            print(f"❌ {username}: User does not exist")
        except Exception as e:
            print(f"❌ {username}: Error - {e}")
