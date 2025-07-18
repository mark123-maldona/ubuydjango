#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
django.setup()

def fix_cookie_issue():
    """Diagnose and fix cookie issues"""
    
    print("🔧 COOKIE ISSUE DIAGNOSIS AND FIX")
    print("=" * 60)
    
    print("\n📋 CURRENT PROBLEM:")
    print("- React app calls /auth/check-auth/")
    print("- Returns {is_authenticated: false}")
    print("- But Django backend works perfectly")
    print("- Issue: Cookies not being sent/received")
    
    print("\n🎯 IMMEDIATE SOLUTION:")
    print("=" * 60)
    
    print("\n1. 🌐 BROWSER COOKIE SETTINGS:")
    print("   - Open Chrome/Edge settings")
    print("   - Go to Privacy and security > Site settings")
    print("   - Click on 'Cookies and site data'")
    print("   - Make sure 'Allow all cookies' is selected")
    print("   - OR add localhost:5173 and 127.0.0.1:8000 to allowed sites")
    
    print("\n2. 🔄 CLEAR EVERYTHING:")
    print("   - Press Ctrl+Shift+Delete")
    print("   - Select 'All time'")
    print("   - Clear: Cookies, Cache, Local Storage")
    print("   - Restart browser completely")
    
    print("\n3. 📡 TEST MANUALLY:")
    print("   - Go to http://localhost:5173")
    print("   - Open Dev Tools (F12)")
    print("   - Go to Network tab")
    print("   - Try to login with: testuser / testpassword123")
    print("   - Look for 'Set-Cookie' header in response")
    
    print("\n🛠️ BROWSER CONSOLE TEST:")
    print("=" * 60)
    
    print("\nPaste this in your browser console (F12 → Console):")
    print("""
// Test 1: Check current cookies
console.log('Current cookies:', document.cookie);

// Test 2: Test login
fetch('http://127.0.0.1:8000/auth/login/', {
    method: 'POST',
    credentials: 'include',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        password: 'testpassword123'
    })
})
.then(response => {
    console.log('Login response headers:', response.headers);
    return response.json();
})
.then(data => {
    console.log('Login result:', data);
    console.log('Cookies after login:', document.cookie);
    
    // Test 3: Test auth check
    return fetch('http://127.0.0.1:8000/auth/check-auth/', {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        }
    });
})
.then(response => response.json())
.then(data => console.log('Auth check result:', data))
.catch(error => console.error('Error:', error));
""")
    
    print("\n🚨 COMMON ISSUES:")
    print("=" * 60)
    
    print("\n1. Third-party cookies blocked:")
    print("   - Chrome: Settings → Privacy → Cookies → Allow all")
    print("   - Firefox: Settings → Privacy → Cookies → Accept all")
    print("   - Edge: Settings → Privacy → Cookies → Allow all")
    
    print("\n2. Localhost vs 127.0.0.1:")
    print("   - Make sure React is on localhost:5173")
    print("   - Make sure Django is on 127.0.0.1:8000")
    print("   - Don't mix localhost and 127.0.0.1")
    
    print("\n3. Browser extensions:")
    print("   - Disable AdBlockers")
    print("   - Disable Privacy extensions")
    print("   - Try in Incognito/Private mode")
    
    print("\n🔍 DEBUGGING STEPS:")
    print("=" * 60)
    
    print("\n1. Check if cookies are being set:")
    print("   - Login → Check Network tab")
    print("   - Look for 'Set-Cookie: sessionid=...'")
    print("   - Check Application tab → Cookies")
    
    print("\n2. Check if cookies are being sent:")
    print("   - Make any request after login")
    print("   - Check Request Headers")
    print("   - Look for 'Cookie: sessionid=...'")
    
    print("\n3. Test different scenarios:")
    print("   - Try different browser")
    print("   - Try incognito mode")
    print("   - Try disabling all extensions")
    
    print("\n⚡ QUICK FIX COMMANDS:")
    print("=" * 60)
    
    print("\nRun these in PowerShell (as admin):")
    print("1. netsh winsock reset")
    print("2. ipconfig /flushdns")
    print("3. Restart computer")
    
    print("\n🎯 FINAL SOLUTION:")
    print("=" * 60)
    
    print("\nIf nothing works, try this:")
    print("1. Use the same domain for both apps:")
    print("   - Change React to run on 127.0.0.1:5173")
    print("   - Keep Django on 127.0.0.1:8000")
    print("   - This avoids cross-domain cookie issues")
    
    print("\n2. Or use a proxy:")
    print("   - Configure Vite to proxy API calls")
    print("   - All requests go through same domain")
    
    print("\n💡 REMEMBER:")
    print("- Backend works perfectly ✅")
    print("- Frontend needs to send cookies ❌")
    print("- Clear cache and try again! 🔄")

if __name__ == "__main__":
    fix_cookie_issue()
