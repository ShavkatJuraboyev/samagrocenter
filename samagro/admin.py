from django.contrib import admin
from samagro.models import ProductCategory, Products, ProductPicture, Users, Order
# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',  'parent')  # Ko'rsatiladigan ustunlar
    list_filter = ('parent',)  # Filtrlar uchun 'parent' ni to'g'ri qo'llash
    search_fields = ('name',)  # Qidiruv maydonlari

admin.site.register(ProductPicture)

@admin.register(Products)  
class ProductsAdmin(admin.ModelAdmin): 
    list_display = ('name', 'price', 'created_at')  


admin.site.register(Users)
admin.site.register(Order)