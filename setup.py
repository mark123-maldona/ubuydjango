#!/usr/bin/env python
"""
Setup script for U-Buy Django project
This script will:
1. Run migrations
2. Populate categories
3. Populate sellers
4. Create a superuser (optional)
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_project():
    """Setup the Django project"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_buy.settings')
    django.setup()
    
    print("🚀 Setting up U-Buy Django project...")
    print("=" * 50)
    
    # Run migrations
    print("1. Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Populate categories
    print("\n2. Populating categories...")
    execute_from_command_line(['manage.py', 'populate_categories'])
    
    # Populate sellers
    print("\n3. Populating sellers...")
    execute_from_command_line(['manage.py', 'populate_sellers'])
    
    # Create superuser
    print("\n4. Creating superuser...")
    print("You can create a superuser to access the admin panel:")
    print("Run: python manage.py createsuperuser")
    
    print("\n✅ Setup complete!")
    print("=" * 50)
    print("🎉 Your U-Buy Django project is ready!")
    print("To start the server, run: python manage.py runserver")
    print("Admin panel: http://127.0.0.1:8000/myadmin/")
    print("API endpoints:")
    print("  - GET  http://127.0.0.1:8000/store/          (List products)")
    print("  - POST http://127.0.0.1:8000/store/create/   (Create product)")

if __name__ == '__main__':
    setup_project()
