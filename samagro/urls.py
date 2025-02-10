from django.urls import path
from samagro.views import (
    home, shop, about, contact, shop_view, register, 
    verify_sms, checkout, profile, logout_view,
    login_view, remove_from_cart, add_to_cart, cart,
    resend_code
    )


urlpatterns = [
    path('', home, name='home'),

    path('shop/', shop, name='shop'),
    path('shop/<int:pk>/view/', shop_view, name='shop_view'),
    path('cart/view/', cart, name='cart'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('register/', register, name='register'),
    path('verify/', verify_sms, name='verify'),
    path('login/',login_view, name='login'),


    path('checkout/', checkout, name='checkout'),
    # path('confirm/order/', confirm_order, name='confirm_order'),

    path('profile/', profile, name='profile'),  # Profil sahifasi
    path('logout/', logout_view, name='logout'),  # Logout sahifasi

    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    path("resend-code/", resend_code, name="resend_code"),
]
