import requests
import os

# Test POST endpoint with form data
url = 'http://127.0.0.1:8000/store/create/'

# Create a test image file
with open('test_image.jpg', 'wb') as f:
    f.write(b'fake image content')

# Test data
data = {
    'Productname': 'Test Product',
    'product_description': 'This is a test product description',
    'initial_price': '100',
    'currtent_price': '80',
    'discount': '20',
    'stock': '10',
    'seller': '1',
    'is_discounted': 'true',
    'product_category': '1'
}

# Test file
files = {
    'product_image': ('test_image.jpg', open('test_image.jpg', 'rb'), 'image/jpeg')
}

try:
    response = requests.post(url, data=data, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("SUCCESS: Product created successfully!")
    else:
        print("ERROR: Product creation failed!")
        
except Exception as e:
    print(f"Error: {e}")
    
finally:
    # Clean up test file
    if os.path.exists('test_image.jpg'):
        os.remove('test_image.jpg')
