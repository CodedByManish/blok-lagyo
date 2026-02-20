from django.shortcuts import render, get_object_or_404
from .models import Product

# List of all products
def all_products(request):
    products = Product.objects.filter(available=True)
    return render(request, "product_list.html", {"products": products})

# Product detail page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, "product_detail.html", {"product": product})

def restaurant_detail(request, restaurant_name):
    display_name = restaurant_name.replace('-', ' ').title()
    products = Product.objects.filter(restaurant__iexact=display_name, available=True)
    categories = products.values_list('category', flat=True).distinct()
    context = {
        'restaurant_name': display_name,
        'products': products,
        'categories': categories,
    }
    return render(request, 'restaurant.html', context)