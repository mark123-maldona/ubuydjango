#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

from django.contrib.auth.models import User

def check_and_fix_cookie_issue():
    """Check for cookie/session issues and provide fixes"""
    
    print("🔧 FRONTEND COOKIE DEBUGGING AND FIXES")
    print("=" * 60)
    
    # Check if user exists
    user = User.objects.filter(username='testuser').first()
    if not user:
        print("❌ Test user not found. Creating one...")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created user: {user.username}")
    else:
        print(f"✅ Test user exists: {user.username}")
    
    print("\n🔍 COMMON FRONTEND ISSUES AND SOLUTIONS:")
    print("=" * 60)
    
    print("\n1. 🍪 Cookie Domain Issue:")
    print("   Problem: React app can't receive cookies from Django")
    print("   Solution: Check if both apps are running on correct domains")
    print("   - Django: http://127.0.0.1:8000")
    print("   - React: http://localhost:3000")
    
    print("\n2. 🌐 CORS Configuration:")
    print("   Problem: Browser blocks cross-origin requests")
    print("   Solution: Ensure CORS is properly configured")
    print("   ✅ CORS_ALLOW_CREDENTIALS = True")
    print("   ✅ CORS_ALLOWED_ORIGINS includes React app URL")
    
    print("\n3. 🔄 Session Cookie Settings:")
    print("   Problem: Session cookies not being set/sent")
    print("   Solution: Check session settings in Django")
    print("   ✅ SESSION_COOKIE_HTTPONLY = False")
    print("   ✅ SESSION_COOKIE_SAMESITE = None")
    
    print("\n4. 📡 Frontend Request Headers:")
    print("   Problem: React not sending cookies with requests")
    print("   Solution: Always include 'credentials: include' in fetch")
    
    print("\n🎯 IMMEDIATE FIXES TO TRY:")
    print("=" * 60)
    
    print("\n1. Clear browser cache and cookies completely")
    print("2. Restart both Django and React servers")
    print("3. Use these exact URLs:")
    print("   - Django: http://127.0.0.1:8000")
    print("   - React: http://localhost:3000")
    print("4. Test with these credentials:")
    print("   - Username: testuser")
    print("   - Password: testpassword123")
    
    print("\n5. Check browser developer tools:")
    print("   - Network tab: Look for 'Set-Cookie' headers")
    print("   - Application tab: Check if cookies are stored")
    print("   - Console: Look for CORS errors")
    
    print("\n🛠️ TECHNICAL DEBUGGING:")
    print("=" * 60)
    
    print("\nIf still not working, check these in browser dev tools:")
    print("1. After login, check Network tab for Set-Cookie header")
    print("2. Check Application > Cookies for 'sessionid' cookie")
    print("3. Verify subsequent requests include Cookie header")
    print("4. Look for any CORS errors in Console")
    
    print("\n📋 STEP-BY-STEP TESTING:")
    print("=" * 60)
    
    print("\n1. Start Django server: python manage.py runserver")
    print("2. Start React app: npm start (or yarn start)")
    print("3. Open browser to http://localhost:3000")
    print("4. Open Developer Tools (F12)")
    print("5. Go to Network tab")
    print("6. Try to login with testuser/testpassword123")
    print("7. Check if 'Set-Cookie' appears in login response")
    print("8. Check if cookie is sent with next requests")
    
    print("\n🔄 FINAL RESORT:")
    print("=" * 60)
    
    print("If nothing works, try accessing Django admin:")
    print("1. Go to http://127.0.0.1:8000/admin/")
    print("2. Create a superuser if needed")
    print("3. Login to admin to test if cookies work there")
    print("4. If admin works, issue is in React app")
    print("5. If admin doesn't work, issue is in Django settings")

if __name__ == "__main__":
    check_and_fix_cookie_issue()
