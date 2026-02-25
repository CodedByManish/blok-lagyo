import requests
import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from checkout.models import Order

#Paypal imports
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import uuid

# Internal imports
from .models import Order, OrderLineItem
from .forms import OrderForm
from django_esewa import EsewaPayment
from products.models import Product  #

@login_required
@login_required
def checkout(request):
    """
    Main checkout view that handles Form display, eSewa, and COD.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect(reverse('products:index'))

    # Re-calculate totals (always do this on server-side)
    cart_items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = quantity * product.price
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    delivery_fee = (total * Decimal('0.15')).quantize(Decimal('0.01'))
    discount = (total * Decimal('0.05')).quantize(Decimal('0.01'))
    final_total = (total + delivery_fee - discount).quantize(Decimal('0.01'))

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_method = request.POST.get('payment_method') # Get the clicked button value

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user  
            order.total_paid = final_total
            # Optional: if your Order model has a payment_method field, save it:
            # order.payment_method = payment_method 
            order.save()
            
            for item in cart_items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )

            # --- NEW LOGIC FOR CASH ON DELIVERY ---
            if payment_method == 'cod':
                request.session['cart'] = {} # Clear cart
                messages.success(request, f"Order #{order.id} placed successfully via Cash on Delivery!")
                return redirect(reverse('accounts:profile')) # Redirect to profile to see the order

            # --- ESEWA LOGIC (Only runs if not COD) ---
            transaction_uuid = f"ORDER-{order.id}-{int(timezone.now().timestamp())}"
            CORRECT_TEST_KEY = "8gBm/:&EnhH.1/q" 
            
            payment = EsewaPayment(
                product_code="EPAYTEST",
                secret_key=CORRECT_TEST_KEY,
                success_url=request.build_absolute_uri(reverse('checkout:esewa_success')),
                failure_url=request.build_absolute_uri(reverse('checkout:esewa_failure')),
                amount=float(total),
                tax_amount=0.0,
                total_amount=float(final_total),
                product_delivery_charge=float(delivery_fee),
                product_service_charge=0.0,
                transaction_uuid=transaction_uuid
            )
            payment.create_signature()
            esewa_form_html = payment.generate_form()

            context = {
                'esewa_form': esewa_form_html,
                'esewa_url': "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
            }
            return render(request, "redirect_esewa.html", context)
    else:
        order_form = OrderForm()

    # Context for GET request
    context = {
        'order_form': order_form,
        'cart_items': cart_items,
        'total': total,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'final_total': final_total,
    }
    return render(request, "checkout.html", context)

@login_required
def khalti_checkout(request):
    """
    Separate view to handle Khalti initiation.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect(reverse('products:index'))

    # Quick calculation for total
    total = sum(Decimal(str(get_object_or_404(Product, id=pid).price)) * qty for pid, qty in cart.items())
    delivery_fee = (total * Decimal('0.15')).quantize(Decimal('0.01'))
    final_total = total + delivery_fee

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.total_paid = final_total
            order.save()

            # Khalti Payload
            amount_in_paisa = int(float(final_total) * 100)
            url = "https://a.khalti.com/api/v2/epayment/initiate/"
            
            payload = json.dumps({
                "return_url": request.build_absolute_uri(reverse('checkout:khalti_verify')),
                "website_url": request.build_absolute_uri('/'),
                "amount": amount_in_paisa,
                "purchase_order_id": str(order.id),
                "purchase_order_name": f"Order #{order.id}",
                "customer_info": {
                    "name": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                    "phone": "9800000000"
                }
            })
            headers = {
                'Authorization': f'key {settings.KHALTI_SECRET_KEY}',
                'Content-Type': 'application/json',
            }

            response = requests.post(url, headers=headers, data=payload)
            resp_dict = response.json()

            if response.status_code == 200 and "payment_url" in resp_dict:
                return redirect(resp_dict["payment_url"])
            
            messages.error(request, "Khalti failed. " + resp_dict.get('detail', ''))
            return redirect(reverse('checkout:checkout'))

@login_required
def khalti_verify(request):
    pidx = request.GET.get('pidx')
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    headers = {'Authorization': f'key {settings.KHALTI_SECRET_KEY}'}
    
    response = requests.post(url, headers=headers, data=json.dumps({"pidx": pidx}))
    resp_dict = response.json()

    if resp_dict.get("status") == "Completed":
        request.session['cart'] = {}
        messages.success(request, "Paid with Khalti!")
        return redirect(reverse('products:index'))
    
    messages.error(request, "Khalti verification failed.")
    return redirect(reverse('checkout:checkout'))

@login_required
def esewa_success(request):
    request.session['cart'] = {}
    messages.success(request, "Paid with eSewa!")
    return redirect(reverse('products:index'))

@login_required
def esewa_failure(request):
    messages.error(request, "eSewa Payment failed.")
    return redirect(reverse('checkout:checkout'))



#------------------------------------------------
#------------------- PAYPAL VIEWS ------------------
#------------------------------------------------
@login_required
def paypal_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Cart is empty.")
        return redirect('products:index')

    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total += product.price * quantity

    delivery_fee = (total * Decimal('0.15')).quantize(Decimal('0.01'))
    discount = (total * Decimal('0.05')).quantize(Decimal('0.01'))
    final_total = (total + delivery_fee - discount).quantize(Decimal('0.01'))

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.total_paid = final_total
            order.save()

            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            host = request.get_host()

            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": str(final_total),
                "item_name": f"Food Order #{order.id}",
                "invoice": str(order.id),
                "currency_code": "USD",
                "notify_url": f"http://{host}/checkout/paypal/",
                "return_url": f"http://{host}{reverse('checkout:paypal_success')}",
                "cancel_return": f"http://{host}{reverse('checkout:paypal_cancel')}",
                "custom": str(order.id),
            }

            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, "paypal_redirect.html", {"form": form})

    return redirect('checkout:checkout')

@csrf_exempt
@login_required
def paypal_success(request):
    messages.success(request, "Payment completed successfully!")
    request.session['cart'] = {}
    return redirect('products:index')

@csrf_exempt
@login_required
def paypal_cancel(request):
    messages.error(request, "Payment cancelled.")
    return redirect('checkout:checkout')

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    order.delete()
    messages.success(request, f"Order #{order_id} has been cancelled and removed.")
    return redirect('accounts:profile')