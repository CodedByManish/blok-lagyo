"""Food delivery app URL configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fooddelivery.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # authentication
    path('accounts/', include('accounts.urls')),

    # app urls
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include(('checkout.urls', 'checkout'), namespace='checkout')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
