from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from .models import Order

def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:

        # Verify receiver email
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            return

        order_id = ipn_obj.custom

        try:
            order = Order.objects.get(id=order_id)

            if ipn_obj.mc_gross == order.total_paid and ipn_obj.mc_currency == 'USD':
                order.paid = True
                order.save()

        except Order.DoesNotExist:
            pass

valid_ipn_received.connect(paypal_payment_received)