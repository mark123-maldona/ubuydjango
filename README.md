# U-Buy Django Project

This is the backend API for the U-Buy marketplace application.

## Features

- **Product Management**: Create, read, update, and delete products
- **Category System**: Organize products into categories
- **Seller Management**: Handle seller information and products
- **Image Upload**: Support for product images
- **REST API**: Full REST API for frontend integration
- **Admin Panel**: Django admin interface for easy management

## Project Structure

```
u_buy/
├── manage.py
├── requirements.txt
├── setup.py
├── u_buy/                  # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── store/                  # Store app (products, categories)
│   ├── models.py
│   ├── views.py
│   ├── serializer.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           ├── populate_categories.py
│           └── populate_sellers.py
└── users/                  # User management (sellers)
    ├── models.py
    └── ...
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Run database migrations
- Populate categories
- Populate sample sellers
- Provide instructions for creating a superuser

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Products

- **GET** `/store/` - List all products
- **POST** `/store/create/` - Create a new product

### Product Creation

To create a product, send a POST request to `/store/create/` with the following form data:

```json
{
  "Productname": "Product Name",
  "product_description": "Product description",
  "initial_price": 100.00,
  "currtent_price": 80.00,
  "discount": 20.00,
  "product_image": "image_file",
  "stock": 10,
  "seller": 1,
  "is_discounted": true,
  "product_category": 1
}
```

### Product Model Fields

- `Productname`: Product name (required)
- `product_description`: Product description (required)
- `initial_price`: Original price (optional)
- `currtent_price`: Current selling price (required)
- `discount`: Discount percentage (auto-calculated)
- `product_image`: Product image file (required)
- `stock`: Available quantity (default: 1)
- `seller`: Seller ID (foreign key)
- `is_discounted`: Boolean indicating if product is discounted
- `product_category`: Category ID (foreign key)

## Categories

The system comes pre-populated with the following categories:

1. Electronics
2. Clothing
3. Books
4. Home & Garden
5. Sports
6. Beauty
7. Toys
8. Automotive
9. Food
10. Health
11. Music
12. Photography
13. Pets
14. Jewelry
15. Art
16. Kitchen
17. Home Decor
18. Home Furniture
19. Tools
20. Food & Beverages

## Frontend Integration

The API is configured with CORS headers to work with the React frontend. The frontend sell page should send form data to the `/store/create/` endpoint.

### Frontend Form Fields

Make sure your frontend form includes these fields that match the Django model:

- `Productname` (text)
- `product_description` (textarea)
- `initial_price` (number, optional)
- `currtent_price` (number, required)
- `product_image` (file, required)
- `stock` (number, default: 1)
- `seller` (number, default: 1)
- `product_category` (number, default: 1)

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/myadmin/` to:

- View and manage products
- Manage categories
- Manage sellers
- View uploaded images

## File Uploads

Product images are stored in the `media/productimages/` directory. Make sure the `media` directory is properly configured in your deployment.

## Development Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Populate categories
python manage.py populate_categories

# Populate sellers
python manage.py populate_sellers

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Troubleshooting

1. **CORS Issues**: Make sure `django-cors-headers` is installed and configured
2. **File Upload Issues**: Ensure `Pillow` is installed and `MEDIA_ROOT` is configured
3. **Database Issues**: Run migrations with `python manage.py migrate`
4. **Category/Seller Issues**: Run the populate commands to ensure data exists

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL/MySQL)
3. Set up proper media file serving
4. Configure CORS for your frontend domain
5. Set up proper secret key management
