from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    """
    Makes cart contents available in all templates.
    """
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = quantity * product.price
        cart_items.append({
            'id': product.id,
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
        product_count += quantity

    return {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }
