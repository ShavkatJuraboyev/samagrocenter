from django.contrib import admin
from samagro.models import ProductCategory, Products, ProductPicture
# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',  'parent')  # Ko'rsatiladigan ustunlar
    list_filter = ('parent',)  # Filtrlar uchun 'parent' ni to'g'ri qo'llash
    search_fields = ('name',)  # Qidiruv maydonlari

class ProductPictureInline(admin.TabularInline):  
    model = Products.images.through  
    extra = 1  

admin.site.register(ProductPicture)

@admin.register(Products)  
class ProductsAdmin(admin.ModelAdmin):  
    inlines = [ProductPictureInline]  
    list_display = ('name', 'price', 'created_at')  