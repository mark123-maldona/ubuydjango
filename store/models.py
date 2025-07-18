from django.db import models
from users.models import Seller

# This model represents a category for products.
# Categories can be used to group products together for easier navigation and filtering.
class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.category

# This model represents a product in the market.
# Products have a name, description, initial price, current price, discount, image, stock, seller, and category.
# The seller is a foreign key to the Seller model, and the category is a foreign key to the Category model.
class Product(models.Model):
    Productname = models.CharField(max_length=200)
    product_description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currtent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00 , help_text="Discount in percentage", blank=True, null=True)
    product_image = models.ImageField(upload_to='productimages/')
    stock = models.PositiveIntegerField( default=1)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='sellers')
    is_discounted = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='categories', null=True)


    def __str__(self):
        return self.Productname

# This model represents a seller in the market.
# Sellers can list products for sale and manage their inventory.

    
# Create your models here.
