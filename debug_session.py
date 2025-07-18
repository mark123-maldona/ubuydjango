#!/usr/bin/env python3
"""
Debug session and authentication issues
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
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timezone

def debug_sessions():
    """Debug session data"""
    print("🔍 DEBUG SESSION DATA")
    
    # Check all sessions
    sessions = Session.objects.all()
    print(f"\n📊 Total sessions in database: {sessions.count()}")
    
    for session in sessions:
        print(f"\n🔑 Session: {session.session_key}")
        print(f"   Expires: {session.expire_date}")
        print(f"   Expired: {session.expire_date < datetime.now(timezone.utc)}")
        
        # Decode session data
        try:
            session_data = session.get_decoded()
            print(f"   Session data: {session_data}")
            
            # Check if user is logged in
            if '_auth_user_id' in session_data:
                user_id = session_data['_auth_user_id']
                try:
                    user = User.objects.get(id=user_id)
                    print(f"   ✅ User logged in: {user.username} (ID: {user.id})")
                except User.DoesNotExist:
                    print(f"   ❌ User ID {user_id} not found")
            else:
                print("   ❌ No user logged in this session")
                
        except Exception as e:
            print(f"   ❌ Error decoding session: {e}")
    
    # Check specific session
    target_session = "5z8gf9wq03x04w1xxlkfxg417s060tke"
    print(f"\n🎯 CHECKING TARGET SESSION: {target_session}")
    
    try:
        session = Session.objects.get(session_key=target_session)
        print(f"   ✅ Session found")
        print(f"   Expires: {session.expire_date}")
        print(f"   Expired: {session.expire_date < datetime.now(timezone.utc)}")
        
        session_data = session.get_decoded()
        print(f"   Session data: {session_data}")
        
        if '_auth_user_id' in session_data:
            user_id = session_data['_auth_user_id']
            try:
                user = User.objects.get(id=user_id)
                print(f"   ✅ User: {user.username} (ID: {user.id})")
            except User.DoesNotExist:
                print(f"   ❌ User ID {user_id} not found")
        else:
            print("   ❌ No user logged in this session")
            
    except Session.DoesNotExist:
        print(f"   ❌ Session {target_session} not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == '__main__':
    debug_sessions()
