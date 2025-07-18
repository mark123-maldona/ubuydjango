import requests
from PIL import Image

# Create a simple test image
def create_test_image():
    img = Image.new('RGB', (100, 100), color='blue')
    img.save('unified_test.jpg', 'JPEG')
    return 'unified_test.jpg'

# Test POST to the unified endpoint
url = 'http://127.0.0.1:8000/store/'

# Create test image
image_path = create_test_image()

# Test data
data = {
    'Productname': 'Unified Endpoint Test Product',
    'product_description': 'Testing the unified endpoint that handles both GET and POST',
    'initial_price': '150',
    'currtent_price': '120',
    'discount': '20',
    'stock': '5',
    'seller': '1',
    'is_discounted': 'true',
    'product_category': '2'
}

try:
    with open(image_path, 'rb') as f:
        files = {
            'product_image': ('unified_test.jpg', f, 'image/jpeg')
        }
        
        print("Testing POST to unified endpoint...")
        response = requests.post(url, data=data, files=files)
        print(f"POST Status Code: {response.status_code}")
        print(f"POST Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS: Product created successfully!")
            
            # Now test GET to see if the product appears
            print("\nTesting GET to see if product appears...")
            get_response = requests.get(url)
            print(f"GET Status Code: {get_response.status_code}")
            
            if get_response.status_code == 200:
                products = get_response.json()
                print(f"Total products: {len(products)}")
                print("Latest product:", products[-1]['Productname'] if products else "No products")
            
        else:
            print("ERROR: Product creation failed!")
        
except Exception as e:
    print(f"Error: {e}")
    
finally:
    # Clean up test file
    import os
    if os.path.exists(image_path):
        os.remove(image_path)
