"""
Authentication middleware for route protection and session validation
"""
from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
import json
import logging

logger = logging.getLogger(__name__)

class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to protect routes that require authentication
    """
    
    # Define routes that require authentication
    PROTECTED_ROUTES = [
        '/auth/profile/',
        '/auth/logout/',
        '/store/sell/',  # Add the sell page route
        '/store/my-products/',  # Example of other protected routes
        '/users/profile/',
    ]
    
    def process_request(self, request):
        """
        Process incoming requests and check authentication for protected routes
        """
        # First, validate session authentication
        self.validate_session_auth(request)
        
        # Skip authentication check for certain routes
        if self.should_skip_auth_check(request):
            return None
            
        # Check if this is a protected route
        if self.is_protected_route(request.path):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'message': 'You must be logged in to access this resource',
                    'is_authenticated': False,
                    'redirect_to': '/auth/login/'
                }, status=401)
                
        return None
    
    def validate_session_auth(self, request):
        """
        Validate session authentication if user is not already authenticated
        """
        # Only process if user is not already authenticated
        if not request.user.is_authenticated:
            # Check if we have a session cookie
            session_key = request.COOKIES.get('sessionid')
            
            if session_key:
                try:
                    # Get session from database
                    session = Session.objects.get(session_key=session_key)
                    session_data = session.get_decoded()
                    
                    # Check if session has user authentication data
                    if '_auth_user_id' in session_data:
                        user_id = session_data['_auth_user_id']
                        
                        try:
                            user = User.objects.get(id=user_id)
                            
                            # Set the user in the request
                            request.user = user
                            
                            # Update the session if needed
                            if request.session.session_key != session_key:
                                request.session.session_key = session_key
                                request.session['_auth_user_id'] = str(user.id)
                                request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
                                request.session.save()
                            
                            logger.info(f"Session validated: Set user {user.username} from session {session_key}")
                            
                        except User.DoesNotExist:
                            logger.warning(f"Session validation: User {user_id} not found for session {session_key}")
                            
                except Session.DoesNotExist:
                    logger.warning(f"Session validation: Session {session_key} not found")
    
    def should_skip_auth_check(self, request):
        """
        Determine if authentication check should be skipped
        """
        # Skip for public routes
        public_routes = [
            '/auth/login/',
            '/auth/register/',
            '/auth/check-auth/',
            '/store/',  # Public store listing
            '/store/products/',  # Public product listing
        ]
        
        # Skip for static files, admin, etc.
        skip_prefixes = [
            '/static/',
            '/media/',
            '/myadmin/',
            '/admin/',
        ]
        
        # Check public routes
        if request.path in public_routes:
            return True
            
        # Check skip prefixes
        for prefix in skip_prefixes:
            if request.path.startswith(prefix):
                return True
                
        return False
    
    def is_protected_route(self, path):
        """
        Check if a route requires authentication
        """
        for protected_route in self.PROTECTED_ROUTES:
            if path.startswith(protected_route):
                return True
        return False
