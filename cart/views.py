from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from products.models import Product
from decimal import Decimal

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    # Initialize variables at 0 so they always exis
    delivery_fee = Decimal('0.00')
    discount = Decimal('0.00')
    final_total = Decimal('0.00')

    for product_id, quantity in cart.items():
        if quantity < 1:
            continue

        product = get_object_or_404(Product, pk=product_id)
        subtotal = quantity * product.price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total += subtotal
    if total > 0:
        delivery_fee = (total * Decimal('0.15')).quantize(Decimal('0.01'))
        discount = (total * Decimal('0.05')).quantize(Decimal('0.01'))
        final_total = total + delivery_fee - discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'final_total': final_total,
    }

    return render(request, "cart.html", context)


def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

    return redirect(reverse('cart:view_cart'))


def adjust_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    try:
        quantity = int(request.POST.get('quantity', 0))
    except (ValueError, TypeError):
        quantity = 0

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)

    request.session['cart'] = cart

    return redirect(reverse('cart:view_cart'))