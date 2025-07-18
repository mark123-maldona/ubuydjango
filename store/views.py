from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import Product
from .serializer import ProductSerializer, CategorySerializer
from users.models import Seller





def validate_user_session(request):
    """Validate user session and return user object if authenticated"""
    print(f"\n🔍 VALIDATE_USER_SESSION DEBUG:")
    print(f"   Request cookies: {request.COOKIES}")
    print(f"   Django user: {request.user}")
    print(f"   Django user authenticated: {request.user.is_authenticated}")
    
    # First check if Django authentication is working
    if request.user.is_authenticated:
        print(f"   ✅ Django user is authenticated: {request.user.username}")
        return request.user
    
    # Fallback to session validation
    session_key = request.COOKIES.get('sessionid')
    print(f"   Session key from cookies: {session_key}")
    
    if session_key:
        try:
            # Get session from database
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            print(f"   Session data: {session_data}")
            
            # Check if session has user authentication data
            if '_auth_user_id' in session_data:
                user_id = session_data['_auth_user_id']
                user = User.objects.get(id=user_id)
                print(f"   ✅ User found from session: {user.username}")
                
                # Return user
                return user
            else:
                print(f"   ❌ No _auth_user_id in session data")
                return None
        except (Session.DoesNotExist, User.DoesNotExist) as e:
            print(f"   ❌ Session validation error: {e}")
            return None
    
    print(f"   ❌ No session key found")
    return None

@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def store(request):
    if request.method == 'GET':
        # Handle GET request - return all products
        All_products = Product.objects.all()
        serialized_products = ProductSerializer(All_products, many=True)
        return Response(serialized_products.data)
    
    elif request.method == 'POST':
        # Handle POST request - create new product
        # Check if user is authenticated
        user = validate_user_session(request)
        if not user:
            return Response({
                'error': 'Authentication required',
                'message': 'You must be logged in to create products'
            }, status=401)
        
        try:
            print("POST data:", request.POST)
            print("FILES data:", request.FILES)
            print("User:", user.username if user else "Anonymous")
            
            # Get or create a Seller object for the authenticated user
            seller, created = Seller.objects.get_or_create(
                email=user.email,
                defaults={
                    'Sellername': user.username,
                    'phone': ''
                }
            )
            
            print(f"Seller: {seller.Sellername} (ID: {seller.id}), Created: {created}")
            
            # Get data from request.POST and request.FILES
            initial_price = request.POST.get('initial_price')
            current_price = request.POST.get('currtent_price')
            
            # Calculate discount if both prices are provided
            discount = 0.00
            is_discounted = False
            
            if initial_price and current_price:
                try:
                    initial_price_float = float(initial_price)
                    current_price_float = float(current_price)
                    
                    if initial_price_float > current_price_float:
                        discount = ((initial_price_float - current_price_float) / initial_price_float) * 100
                        is_discounted = True
                except (ValueError, ZeroDivisionError):
                    pass
            
            product_data = {
                'Productname': request.POST.get('Productname'),
                'product_description': request.POST.get('product_description'),
                'initial_price': initial_price if initial_price else None,
                'currtent_price': current_price,
                'discount': round(discount, 2),
                'product_image': request.FILES.get('product_image'),
                'stock': request.POST.get('stock', 1),
                'seller': seller.id,
                'is_discounted': is_discounted,
                'product_category': request.POST.get('product_category', 1)
            }
            
            print("Product data:", product_data)
            
            # Validate required fields
            if not product_data['Productname']:
                return Response({'error': 'Product name is required'}, status=400)
            
            if not product_data['product_description']:
                return Response({'error': 'Product description is required'}, status=400)
            
            if not product_data['currtent_price']:
                return Response({'error': 'Current price is required'}, status=400)
            
            if not product_data['product_image']:
                return Response({'error': 'Product image is required'}, status=400)
            
            # Create the product using the serializer
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                product = serializer.save()
                return Response({
                    'message': 'Product created successfully',
                    'product': ProductSerializer(product).data
                }, status=201)
            else:
                print("Serializer errors:", serializer.errors)
                print("Product data being validated:", product_data)
                for field, errors in serializer.errors.items():
                    print(f"Field '{field}' error: {errors}")
                return Response({
                    'error': 'Invalid data',
                    'details': serializer.errors,
                    'received_data': {k: str(v) if k != 'product_image' else 'FILE_UPLOADED' for k, v in product_data.items()}
                }, status=400)
                
        except Exception as e:
            print("Exception:", str(e))
            return Response({
                'error': 'An error occurred while creating the product',
                'details': str(e)
            }, status=500)

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def create_product(request):
    # Check if user is authenticated
    user = validate_user_session(request)
    if not user:
        return Response({
            'error': 'Authentication required',
            'message': 'You must be logged in to create products'
        }, status=401)
    
    try:
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        print("User:", request.user.username if request.user.is_authenticated else "Anonymous")
        
        # Get data from request.POST and request.FILES
        product_data = {
            'Productname': request.POST.get('Productname'),
            'product_description': request.POST.get('product_description'),
            'initial_price': request.POST.get('initial_price') or None,
            'currtent_price': request.POST.get('currtent_price'),
            'discount': request.POST.get('discount', 0.00),
            'product_image': request.FILES.get('product_image'),
            'stock': request.POST.get('stock', 1),
            'seller': request.POST.get('seller', 1),  # Default to seller ID 1
            'is_discounted': request.POST.get('is_discounted', 'false').lower() == 'true',
            'product_category': request.POST.get('product_category', 1)
        }
        
        print("Product data:", product_data)
        
        # Validate required fields
        if not product_data['Productname']:
            return Response({'error': 'Product name is required'}, status=400)
        
        if not product_data['product_description']:
            return Response({'error': 'Product description is required'}, status=400)
        
        if not product_data['currtent_price']:
            return Response({'error': 'Current price is required'}, status=400)
        
        if not product_data['product_image']:
            return Response({'error': 'Product image is required'}, status=400)
        
        # Create the product using the serializer
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                'message': 'Product created successfully',
                'product': ProductSerializer(product).data
            }, status=201)
        else:
            print("Serializer errors:", serializer.errors)
            return Response({
                'error': 'Invalid data',
                'details': serializer.errors
            }, status=400)
            
    except Exception as e:
        print("Exception:", str(e))
        return Response({
            'error': 'An error occurred while creating the product',
            'details': str(e)
        }, status=500)

@csrf_exempt
@api_view(['GET', 'POST'])
def auth_test(request):
    """Test endpoint to debug authentication issues"""
    print(f"\n🔍 AUTH_TEST DEBUG:")
    print(f"   Request method: {request.method}")
    print(f"   Request headers: {dict(request.headers)}")
    print(f"   Request cookies: {request.COOKIES}")
    print(f"   Django user: {request.user}")
    print(f"   Django user authenticated: {request.user.is_authenticated}")
    print(f"   Session key: {request.session.session_key}")
    print(f"   Session data: {dict(request.session)}")
    
    user = validate_user_session(request)
    
    return Response({
        'django_user': str(request.user),
        'django_authenticated': request.user.is_authenticated,
        'session_key': request.session.session_key,
        'session_data': dict(request.session),
        'cookies': dict(request.COOKIES),
        'validated_user': user.username if user else None,
        'validated_user_id': user.id if user else None,
        'validated_user_email': user.email if user else None,
    })
