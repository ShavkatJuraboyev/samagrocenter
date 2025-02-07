from django.urls import path
from samagro.views import home, shop, about, contact


urlpatterns = [
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]
