from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(default=timezone.now)  # <--- default for existing rows

    def __str__(self):
        return self.name

class Product(models.Model):
    restaurant = models.CharField(max_length=100, default="General") 
    category = models.CharField(max_length=100, default="Food")
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Increased max_digits for NPR
    image = models.ImageField(upload_to='images')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.name} ({self.restaurant})"