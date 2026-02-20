from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all()     
    search_query = request.GET.get('search')    
    if search_query:
        products = products.filter(name__icontains=search_query)    
    context = {'products': products,}

    return render(request, 'index.html', context)