from django.urls import path
from .views import register, login_view, logout_view, profile_update, profile, user_update
urlpatterns = [
    path('register/', register, name='register' ),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', profile_update, name='edit_profile'),
    path('edit-user/', user_update, name='edit_user'),
    path('profile/', profile, name='profile')
]