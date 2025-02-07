from django.urls import path
from samagro.views import home, shop, about, contact, shop_view


urlpatterns = [
    path('', home, name='home'),

    path('shop/', shop, name='shop'),
    path('shop/<int:pk>/view', shop_view, name='shop_view'),

    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]
