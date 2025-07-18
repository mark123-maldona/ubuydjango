from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        
        # Extract user data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validate required fields
        if not username or not email or not password:
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'error': f'Registration failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    """Enhanced login with better session management"""
    try:
        print(f"\n🔑 ENHANCED LOGIN DEBUG:")
        print(f"   Request method: {request.method}")
        print(f"   Request headers: {dict(request.headers)}")
        print(f"   Request cookies: {request.COOKIES}")
        
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        print(f"   Login attempt for: {username}")
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"   ✅ User authenticated: {user.username}")
            
            # Login user
            login(request, user)
            
            # Get session info
            session_key = request.session.session_key
            print(f"   Session key: {session_key}")
            print(f"   Session data: {dict(request.session)}")
            
            # Create response
            response_data = {
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_authenticated': True,
                'session_key': session_key
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            
            # Ensure session cookie is set properly
            if session_key:
                print(f"   🍪 Setting session cookie: {session_key}")
                response.set_cookie(
                    'sessionid', 
                    session_key,
                    max_age=604800,  # 1 week
                    httponly=False,
                    secure=False,
                    samesite=None,
                    domain=None,  # Let browser decide
                    path='/'
                )
                print(f"   🍪 Cookie set with domain=None, path=/, httponly=False, samesite=None")
            
            print(f"   ✅ Login successful, session: {session_key}")
            return response
            
        else:
            print(f"   ❌ Authentication failed")
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"   ❌ Login error: {str(e)}")
        return Response({
            'error': f'Login failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'GET'])
def logout_user(request):
    """Logout user"""
    try:
        print(f"\n🔓 LOGOUT DEBUG:")
        print(f"   User before logout: {request.user}")
        print(f"   Is authenticated: {request.user.is_authenticated}")
        print(f"   Session key: {request.session.session_key}")
        
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            
            # Clear session data
            request.session.flush()
            
            print(f"   ✅ User {username} logged out successfully")
            print(f"   Session after logout: {request.session.session_key}")
            
            response = Response({
                'message': 'Logout successful',
                'is_authenticated': False
            }, status=status.HTTP_200_OK)
            
            # Clear session cookie
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
            
            return response
        else:
            print(f"   ❌ User not authenticated")
            return Response({
                'message': 'User not authenticated',
                'is_authenticated': False
            }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"   ❌ Logout error: {str(e)}")
        return Response({
            'error': f'Logout failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def user_profile(request):
    """Enhanced profile view with session validation"""
    try:
        print(f"\n👤 ENHANCED PROFILE DEBUG:")
        print(f"   Session key: {request.session.session_key}")
        print(f"   User: {request.user}")
        print(f"   Is authenticated: {request.user.is_authenticated}")
        
        # Check cookie session manually if user not authenticated
        if not request.user.is_authenticated:
            cookie_session = request.COOKIES.get('sessionid')
            if cookie_session:
                try:
                    session = Session.objects.get(session_key=cookie_session)
                    session_data = session.get_decoded()
                    
                    if '_auth_user_id' in session_data:
                        user_id = session_data['_auth_user_id']
                        user = User.objects.get(id=user_id)
                        
                        # Return user data even if Django auth middleware missed it
                        return Response({
                            'user_id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_authenticated': True,
                            'date_joined': user.date_joined.isoformat(),
                            'session_key': cookie_session
                        }, status=status.HTTP_200_OK)
                        
                except (Session.DoesNotExist, User.DoesNotExist):
                    pass
        
        # Standard authentication check
        if request.user.is_authenticated:
            user = request.user
            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_authenticated': True,
                'date_joined': user.date_joined.isoformat(),
                'session_key': request.session.session_key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User not authenticated',
                'is_authenticated': False
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception as e:
        print(f"   ❌ Profile error: {str(e)}")
        return Response({
            'error': f'Failed to get profile: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def check_auth_status(request):
    """Enhanced authentication check with detailed debugging"""
    try:
        print(f"\n🔍 ENHANCED AUTH CHECK DEBUG:")
        print(f"   Request method: {request.method}")
        print(f"   Request headers: {dict(request.headers)}")
        print(f"   Request cookies: {request.COOKIES}")
        print(f"   Session key: {request.session.session_key}")
        print(f"   User: {request.user}")
        print(f"   Is authenticated: {request.user.is_authenticated}")
        print(f"   Session data: {dict(request.session)}")
        
        # Import Session model for manual validation
        from django.contrib.sessions.models import Session
        
        # Check if session exists in database
        session_key = request.session.session_key
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                session_data = session.get_decoded()
                print(f"   DB Session found: {session_data}")
            except Session.DoesNotExist:
                print(f"   ❌ Session not found in database")
        
        # Check cookie session
        cookie_session = request.COOKIES.get('sessionid')
        if cookie_session:
            print(f"   Cookie session: {cookie_session}")
            try:
                session = Session.objects.get(session_key=cookie_session)
                session_data = session.get_decoded()
                print(f"   Cookie session data: {session_data}")
                
                if '_auth_user_id' in session_data:
                    user_id = session_data['_auth_user_id']
                    try:
                        user = User.objects.get(id=user_id)
                        print(f"   👤 User from session: {user.username}")
                        
                        # If user is not authenticated but session exists, return user data
                        if not request.user.is_authenticated:
                            print(f"   🔄 Returning user from session validation")
                            return Response({
                                'is_authenticated': True,
                                'user_id': user.id,
                                'username': user.username,
                                'email': user.email,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'session_key': cookie_session
                            }, status=status.HTTP_200_OK)
                        
                    except User.DoesNotExist:
                        print(f"   ❌ User ID {user_id} not found")
                        
            except Session.DoesNotExist:
                print(f"   ❌ Cookie session not found in database")
        
        # Final check
        if request.user.is_authenticated:
            user_data = {
                'is_authenticated': True,
                'user_id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'session_key': request.session.session_key
            }
            print(f"   ✅ Returning authenticated user: {user_data['username']}")
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            print(f"   ❌ User not authenticated")
            return Response({
                'is_authenticated': False,
                'session_key': request.session.session_key,
                'cookie_session': cookie_session
            }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"   ❌ Error in enhanced auth check: {str(e)}")
        return Response({
            'error': f'Failed to check auth status: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_token(request):
    """Get CSRF token for frontend"""
    try:
        csrf_token = get_token(request)
        return Response({
            'csrf_token': csrf_token,
            'message': 'CSRF token retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': f'Failed to get CSRF token: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
