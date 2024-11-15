from django.urls import path
from .views import (campaign_view,home, donation, default_donation_page,
                     process_payment, payment_success, about_view)
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('campaign/', campaign_view , name='campaign'),
    path('', home, name='home'),
    path('donate/', default_donation_page, name='donationpage'), 
    path('donate/<int:campaign_id>/', donation, name='donate' ),
    path('process-payment/<str:amount>/<int:campaign_id>', process_payment, name='process_payment'),
    path('payment-success/', payment_success, name='payment_success' ),
    path('about/', about_view, name='about')
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)