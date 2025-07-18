from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Populate categories for the store'

    def handle(self, *args, **options):
        categories = [
            'Electronics',
            'Clothing',
            'Books',
            'Home & Garden',
            'Sports',
            'Beauty',
            'Toys',
            'Automotive',
            'Food',
            'Health',
            'Music',
            'Photography',
            'Pets',
            'Jewelry',
            'Art',
            'Kitchen',
            'Home Decor',
            'Home Furniture',
            'Tools',
            'Food & Beverages'
        ]

        for category_name in categories:
            category, created = Category.objects.get_or_create(category=category_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category: {category_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category_name}')
                )

        self.stdout.write(self.style.SUCCESS('Categories populated successfully!'))
