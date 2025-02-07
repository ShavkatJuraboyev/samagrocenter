from django.shortcuts import render
from samagro.models import ProductCategory, Products
# Create your views here.



def home(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    context = {
        'product_categorys': product_categorys,
    }
    return render(request, 'home/index.html', context=context)

def shop(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    products = Products.objects.all()
    context = {
        'product_categorys': product_categorys,
        "products":products,
    }
    return render(request, 'home/shop.html', context=context)


def about(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    context = {
        'product_categorys': product_categorys,
    }
    return render(request, 'home/about.html', context=context)

def contact(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    context = {
        'product_categorys': product_categorys,
    }
    return render(request, 'home/contact.html', context=context)