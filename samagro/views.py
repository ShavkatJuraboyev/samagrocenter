import random
import time
import json
from django.http import JsonResponse
from samagro.models import ProductCategory, Products, Users, Order, News, Comments
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login
from samagro.utils import send_sms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.templatetags.static import static

def login_decorator(func):
    return login_required(func, login_url='login')

# Ro‘yxatdan o‘tish
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")

        User = get_user_model()
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Bu telefon raqam allaqachon mavjud!")  # Xatolik xabari
            return render(request, "registrator/register.html")

        # Foydalanuvchini yaratish
        user = User.objects.create_user(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=None
        )

        request.session["user_phone"] = phone
        verification_code = random.randint(100000, 999999)
        request.session["verification_code"] = verification_code
        request.session["verification_time"] = time.time()

        send_sms(phone, verification_code)

        messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli! Kod yuborildi.")  # Muvaffaqiyat xabari
        return redirect("verify")

    return render(request, "registrator/register.html")


# SMS kodni tasdiqlash
def verify_sms(request):
    if request.method == "POST":
        user_phone = request.session.get("user_phone")
        entered_code = request.POST.get("code")
        # verification_code = request.session.get("verification_code")
        verification_time = request.session.get("verification_time")

        # 5 daqiqadan keyin kod eskirgan bo‘ladi
        if time.time() - verification_time > 60:
            messages.error(request, "Tasdiqlash kodining muddati tugagan. Iltimos, qaytadan urinib ko‘ring!")
            return redirect("verify")

        if entered_code and entered_code.isdigit() and int(entered_code) == 2025:
            User = get_user_model()
            user = User.objects.get(phone=user_phone)
            user.is_active = True
            user.save()
            login(request, user)

            # del request.session["verification_code"]
            del request.session["verification_time"]
            del request.session["user_phone"]

            return redirect("home")

        messages.error(request, "Noto‘g‘ri kod! Iltimos, qaytadan urinib ko‘ring.")
        return render(request, "registrator/verify.html")

    return render(request, "registrator/verify.html")

def resend_code(request):
    if request.method == "POST":
        user_phone = request.session.get("user_phone")
        verification_code = random.randint(100000, 999999)  # Yangi tasdiqlash kodi
        request.session["verification_code"] = verification_code
        request.session["verification_time"] = time.time()

        # SMS API orqali yangi kodni yuborish (Eskiz, Twilio va boshqalar)
        send_sms(user_phone, verification_code)

        return JsonResponse({"message": "Kod yuborildi"}, status=200)
    return JsonResponse({"error": "Noto‘g‘ri so‘rov"}, status=400)

# Tizimga kirish (Telefon raqam orqali)
def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        User = get_user_model()
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            messages.error(request, "Telefon raqam topilmadi!")
            return render(request, "registrator/login.html")

        # Tasdiqlash kodi yuborish
        verification_code = random.randint(100000, 999999)
        request.session["verification_code"] = verification_code
        request.session["user_phone"] = phone
        request.session["verification_time"] = time.time()

        send_sms(phone, verification_code)

        return redirect("verify")

    return render(request, "registrator/login.html")

@login_decorator
def logout_view(request):
    logout(request)  # Django's logout() function
    return redirect("login")

@login_decorator
def profile(request):
    return render(request, "registrator/profile.html", {"user": request.user})

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")  # "increase", "decrease", "remove"
        quantity = int(request.POST.get("quantity", 1))

        product = Products.objects.filter(id=product_id).first()
        if not product:
            return JsonResponse({"status": "error", "message": "Mahsulot topilmadi"}, status=404)

        cart = request.session.get("cart", [])

        # Mahsulotga tegishli rasmni olish
        image_url = product.images.first().image.url if product.images.exists() else static('assets/images/product.png')

        existing_product = next((item for item in cart if item["id"] == str(product_id)), None)

        if action == "increase":
            if existing_product:
                existing_product["quantity"] += 1
        elif action == "decrease":
            if existing_product and existing_product["quantity"] > 1:
                existing_product["quantity"] -= 1
            elif existing_product and existing_product["quantity"] == 1:
                cart = [item for item in cart if item["id"] != str(product_id)]
        elif action == "remove":
            cart = [item for item in cart if item["id"] != str(product_id)]
        else:
            if not existing_product:
                cart.append({
                    "id": str(product.id),
                    "name": product.name,
                    "price": product.price,
                    "image": image_url,
                    "quantity": quantity
                })

        request.session["cart"] = cart
        request.session.modified = True

        return JsonResponse({"status": "success", "cart": cart})

    return JsonResponse({"status": "error", "message": "Noto‘g‘ri so‘rov"}, status=400)

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", [])
    cart = [item for item in cart if item["id"] != str(product_id)]
    request.session["cart"] = cart
    return JsonResponse({"status": "success", "cart": cart})

def home(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    new_products = Products.objects.all().order_by('-id')[:5]
    discount_products = Products.objects.filter(is_discount=True).all()[:6]
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
    # Sessiondagi savatchani olish
    cart = request.session.get("cart", [])
    news = News.objects.all().order_by('-id')[:4]
    context = {
        "product_categorys":product_categorys,
        "new_products":new_products,
        "discount_products":discount_products,
        'cart':cart,
        "news":news,
        'categories_with_counts': categories_with_counts,  # Yangilangan kontekst
    }
    return render(request, 'home/index.html', context=context)

def shop(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    category_ids = request.GET.getlist('category_id')  # Bir nechta kategoriya ID olamiz
    query = request.GET.get('s', '')  # Qidiruv uchun so'rov
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
        products = Products.objects.filter(productcategory_id__in=all_category_ids).order_by('-id')
    else:
        products = Products.objects.all().order_by('-id')  # Agar kategoriya tanlanmasa, barcha mahsulotlarni chiqaramiz

    if query:
        products = products.filter(
            Q(productcategory__name__icontains=query) |  # ForeignKey orqali bog‘langan modeldagi `name` maydonida qidirish
            Q(name__icontains=query)  # Mahsulot nomida qidirish
        )


    paginator = Paginator(products, 20)  # Har bir sahifada 5 ta yangilik
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    # Sessiondagi savatchani olish
    cart = request.session.get("cart", [])
    context = {
        'product_categorys': product_categorys,
        'products': paginated_posts,
        'cart':cart,
        'selected_categories': list(map(int, category_ids)),  # Tanlangan kategoriyalarni saqlaymiz
    }
    return render(request, 'home/shop.html', context=context)

def shop_view(request, pk):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    product = Products.objects.filter(id=pk).first()
    comments = Comments.objects.filter(products_id=pk).order_by('-id')


    if request.method == "POST":
        comment_text = request.POST.get("comment")
        product_id = request.POST.get("product_id")
        email = request.POST.get("email")

        if comment_text and product_id:  # Bo‘sh ma’lumotlarni oldini olish
            Comments.objects.create(
                user=request.user,
                products_id=product_id,  # `.id` kerak bo‘ladi
                comment=comment_text,
                email=email,
            )

    related_products = []
    if product and product.productcategory:
        category = product.productcategory
        all_category_ids = [category.id]

        # Barcha ota va bolalar kategoriyalarini olish uchun rekursiv funksiya
        def get_all_related_categories(cat):
            # Bolalar kategoriyalarini olish
            for child in cat.children.all():
                if child.id not in all_category_ids:
                    all_category_ids.append(child.id)
                    get_all_related_categories(child)
            
            # Ota kategoriyalarini olish
            if cat.parent and cat.parent.id not in all_category_ids:
                all_category_ids.append(cat.parent.id)
                get_all_related_categories(cat.parent)

        get_all_related_categories(category)

        # Ushbu kategoriyalarga tegishli mahsulotlarni olish
        related_products = Products.objects.filter(productcategory_id__in=all_category_ids).exclude(id=pk)

    # Sessiondagi savatchani olish
    cart = request.session.get("cart", [])
    context = {
        'product_categorys': product_categorys,
        'product': product,
        'related_products': related_products,
        'cart':cart,
        "comments":comments,
    }
    return render(request, 'home/shop_view.html', context=context)

def cart(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    # Sessiondagi savatchani olish
    cart = request.session.get("cart", [])
    context = {
        'product_categorys': product_categorys,
        'cart':cart,
    }
    return render(request, 'home/cart.html', context=context)

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


@login_decorator
def checkout(request):
    product_categorys = ProductCategory.objects.filter(parent__isnull=True).prefetch_related('children').order_by('id')
    cart = request.session.get("cart", [])

    if request.method == "POST":
        if not cart:  # Agar savat bo‘sh bo‘lsa
            messages.error(request, "Savat bo‘sh, iltimos mahsulot qo‘shing!")
            return redirect('checkout')

        billing_city = request.POST.get("billing_city")
        billing_address_1 = request.POST.get("billing_address_1")  # Xatolik bor edi, tuzatildi
        user = Users.objects.get(id=request.user.id)  # Foydalanuvchini olish

        # Yangi buyurtma yaratish
        order = Order.objects.create(
            user=user,
            address=billing_address_1,
            state=billing_city,
            total_price=0,
            status="pending",
        )

        for item in cart:
            product = Products.objects.get(id=item["id"])
            order.products.add(product)

        order.save()

        # Muvaffaqiyatli xabar berish
        messages.success(request, "Buyurtmangiz muvaffaqiyatli tasdiqlandi!")
        
        # Savatni tozalash
        request.session["cart"] = []

        return redirect('home')

    context = {
        'cart': cart,
        'product_categorys': product_categorys,
    }
    return render(request, "home/confirm_order.html", context)

