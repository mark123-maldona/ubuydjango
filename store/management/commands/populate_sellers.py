from django.core.management.base import BaseCommand
from users.models import Seller

class Command(BaseCommand):
    help = 'Populate sellers for the store'

    def handle(self, *args, **options):
        sellers = [
            {'name': 'Tech Store', 'email': 'tech@example.com', 'phone': '0712345678'},
            {'name': 'Fashion Hub', 'email': 'fashion@example.com', 'phone': '0723456789'},
            {'name': 'Book World', 'email': 'books@example.com', 'phone': '0734567890'},
            {'name': 'Home & Garden Plus', 'email': 'home@example.com', 'phone': '0745678901'},
            {'name': 'Sports Pro', 'email': 'sports@example.com', 'phone': '0756789012'},
        ]

        for seller_data in sellers:
            seller, created = Seller.objects.get_or_create(
                email=seller_data['email'],
                defaults={
                    'Sellername': seller_data['name'],
                    'phone': seller_data['phone']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created seller: {seller_data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Seller already exists: {seller_data["name"]}')
                )

        self.stdout.write(self.style.SUCCESS('Sellers populated successfully!'))
