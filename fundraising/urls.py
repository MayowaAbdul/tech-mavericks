from django.urls import path
from .views import (campaign_view,home, donation, default_donation_page,
                     process_payment, payment_success, about_view, team, causes,
                    event, withdraw_view, payment_failed, campaign_info)
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home, name='home'),
    path('campaign/', campaign_view , name='campaign'),
    path('campaign-info/', campaign_info, name='campaigninfo'),
    path('donate/', default_donation_page, name='donationpage'), 
    path('donate/<int:campaign_id>/', donation, name='donate' ),
    path('process-payment/<str:amount>/<int:campaign_id>', process_payment, name='process-payment'),
    path('payment-success/', payment_success, name='payment_success' ),
    path('payment-failed/', payment_failed, name='payment_failed'),
    path('about/', about_view, name='about'),
    path('team/', team, name='team'),
    path('causes/', causes, name='causes'),
    path('event/', event, name='event'),
    path('withdraw/', withdraw_view, name='withdraw')
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   