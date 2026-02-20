from django.urls import path
from .views import all_products, product_detail, restaurant_detail

app_name = 'products' 
urlpatterns = [
    path('', all_products, name='products'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<str:restaurant_name>/', restaurant_detail, name='restaurant_detail'), 

]
