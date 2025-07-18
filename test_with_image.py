import requests
import os
from PIL import Image

# Create a simple test image
def create_test_image():
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    img.save('test_product.jpg', 'JPEG')
    return 'test_product.jpg'

# Test POST endpoint with real image
url = 'http://127.0.0.1:8000/store/create/'

# Create test image
image_path = create_test_image()

# Test data
data = {
    'Productname': 'Test Product via Script',
    'product_description': 'This is a test product created via script',
    'initial_price': '100',
    'currtent_price': '80',
    'discount': '20',
    'stock': '10',
    'seller': '1',
    'is_discounted': 'true',
    'product_category': '1'
}

# Test file
try:
    with open(image_path, 'rb') as f:
        files = {
            'product_image': ('test_product.jpg', f, 'image/jpeg')
        }
        
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
    if os.path.exists(image_path):
        os.remove(image_path)
