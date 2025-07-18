from django.urls import path
from .views import *


urlpatterns = [
    # Define your store URLs here
    path('', store),
    path('create/', create_product),
    path('auth-test/', auth_test),
]
