import requests

# Simple test to trigger the debug output
url = 'http://127.0.0.1:8000/store/create/'

# Just test with minimal data to see the debug output
data = {
    'Productname': 'Test Product',
    'product_description': 'Test description',
    'currtent_price': '100'
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
