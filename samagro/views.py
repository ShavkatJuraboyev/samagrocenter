from django.shortcuts import render
from samagro.models import ProductCategory, Products
from django.core.paginator import Paginator
# Create your views here.



def home(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')

    def get_all_child_categories(category):
        """Ota kategoriya uchun barcha ichki (bola) kategoriyalar ID larini qaytaradi"""
        child_ids = [category.id]
        for child in category.children.all():
            child_ids.extend(get_all_child_categories(child))
        return child_ids

    categories_with_counts = []
    for category in product_categorys:
        all_category_ids = get_all_child_categories(category)  # Ota kategoriya + barcha bolalar
        product_count = Products.objects.filter(productcategory_id__in=all_category_ids).count()  # Ushbu kategoriyaga bog‘liq mahsulotlar soni
        categories_with_counts.append({
            'category': category,
            'product_count': product_count
        })

    context = {
        'categories_with_counts': categories_with_counts,  # Yangilangan kontekst
    }
    return render(request, 'home/index.html', context=context)


def shop(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    category_ids = request.GET.getlist('category_id')  # Bir nechta kategoriya ID olamiz

    if category_ids:
        all_category_ids = []  # Barcha tanlangan kategoriya va ularning bolalarini saqlash

        # Har bir tanlangan kategoriya uchun rekursiv bolalarini topamiz
        def get_all_child_categories(category):
            all_category_ids.append(category.id)
            for child in category.children.all():
                get_all_child_categories(child)

        # Har bir tanlangan kategoriya uchun rekursiyani ishga tushiramiz
        for category_id in category_ids:
            try:
                category = ProductCategory.objects.get(id=category_id)
                get_all_child_categories(category)
            except ProductCategory.DoesNotExist:
                continue

        # Tanlangan kategoriya yoki ularning bolalariga tegishli mahsulotlarni olish
        products = Products.objects.filter(productcategory_id__in=all_category_ids)
    else:
        products = Products.objects.all()  # Agar kategoriya tanlanmasa, barcha mahsulotlarni chiqaramiz


    paginator = Paginator(products, 6)  # Har bir sahifada 5 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    context = {
        'product_categorys': product_categorys,
        'products': paginated_posts,
        'selected_categories': list(map(int, category_ids)),  # Tanlangan kategoriyalarni saqlaymiz
    }
    return render(request, 'home/shop.html', context=context)

def shop_view(request, pk):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    product = Products.objects.filter(id=pk).first()

    related_products = []
    if product and product.productcategory:
        category = product.productcategory
        all_category_ids = [category.id]

        # Rekursiv ravishda barcha ichki kategoriyalarni olish
        def get_all_child_categories(cat):
            for child in cat.children.all():
                all_category_ids.append(child.id)
                get_all_child_categories(child)

        get_all_child_categories(category)

        # Ushbu kategoriyalarga bog‘liq barcha mahsulotlarni olish
        related_products = Products.objects.filter(productcategory_id__in=all_category_ids).exclude(id=pk)

    context = {
        'product_categorys': product_categorys,
        'product': product,
        'related_products': related_products,  # Shu mahsulot kategoriyasiga tegishli mahsulotlar
    }
    return render(request, 'home/shop_view.html', context=context)



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