from django.urls import path
from .views import campaign_view,home, donation, default_donation_page

urlpatterns = [
    path('campaign/', campaign_view , name='campaign'),
    path('', home, name='home'),
    path('donate/', default_donation_page, name='donation_page'), 
    path('donate/<int:campaign_id>/', donation, name='donate' )
]