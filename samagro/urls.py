from django.urls import path
from samagro.views import (
    home, shop, about, contact, shop_view, register, 
    verify_sms, checkout, confirm_order, profile, logout_view,
    login_view, verify_login_sms
    )


urlpatterns = [
    path('', home, name='home'),

    path('shop/', shop, name='shop'),
    path('shop/<int:pk>/view', shop_view, name='shop_view'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('register/', register, name='register'),
    path('verify/', verify_sms, name='verify'),
    path('login/',login_view, name='login'),
    path('verify/', verify_login_sms, name='verify_login'),


    path('checkout/', checkout, name='checkout'),
    path('confirm_order/', confirm_order, name='confirm_order'),

    path('profile/', profile, name='profile'),  # Profil sahifasi
    path('logout/', logout_view, name='logout'),  # Logout sahifasi
]
