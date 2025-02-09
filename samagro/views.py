from samagro.models import ProductCategory, Products, Users, Order
from django.core.paginator import Paginator
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from samagro.utils import send_sms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import get_user_model


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        
        # Telefon raqamining mavjudligini tekshirish
        if Users.objects.filter(phone=phone).exists():
            return render(request, "registrator/register.html", {"error": "Bu telefon raqam allaqachon mavjud!"})

        # Yangi foydalanuvchi yaratish
        user = Users.objects.create(first_name=first_name, last_name=last_name, phone=phone)
        request.session["user_phone"] = phone

        # Tasdiqlash kodi yaratish va SMS yuborish
        verification_code = random.randint(1000, 9999)
        request.session["verification_code"] = verification_code
        send_sms(phone, verification_code)

        return redirect("verify")

    return render(request, "registrator/register.html")

# SMS kodini tasdiqlash
def verify_sms(request):
    if request.method == "POST":
        user_phone = request.session.get("user_phone")
        entered_code = request.POST.get("code")
        verification_code = request.session.get("verification_code")

        # Kodni tekshirish
        if int(entered_code) == verification_code:
            user = Users.objects.get(phone=user_phone)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("home")

        return render(request, "registrator/verify.html", {"error": "Kod noto‘g‘ri!"})

    return render(request, "registrator/verify.html")

# Login (telefon raqami orqali)
def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        
        # Telefon raqamini tekshirish
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            messages.error(request, "Telefon raqam topilmadi!")
            return render(request, "registrator/login.html")
        
        # SMS kodini yuborish
        return send_verification_code(request, phone)

    return render(request, "registrator/login.html")

# SMS kodi yuborish
def send_verification_code(request, phone):
    verification_code = random.randint(1000, 9999)
    request.session["verification_code"] = verification_code
    request.session["user_phone"] = phone

    # SMS yuborish
    send_sms(phone, verification_code)

    return render(request, "registrator/verify_login_sms.html", {"phone": phone})

# SMS kodni tekshirish
def verify_login_sms(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        verification_code = request.session.get("verification_code")
        user_phone = request.session.get("user_phone")

        if not verification_code or not user_phone:
            messages.error(request, "Tasdiqlash kodining muddati tugagan. Iltimos, qaytadan urinib ko‘ring!")
            return redirect("login")

        if entered_code and entered_code.isdigit() and int(entered_code) == verification_code:
            User = get_user_model()
            try:
                user = User.objects.get(phone=user_phone)
                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Qo‘lda backend berildi
                    login(request, user)

                    del request.session["verification_code"]
                    del request.session["user_phone"]

                    return redirect("home")
                else:
                    messages.error(request, "Foydalanuvchi tasdiqlanmagan!")
                    return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "Foydalanuvchi topilmadi!")
                return redirect("login")

        messages.error(request, "Noto‘g‘ri kod! Iltimos, qayta urinib ko‘ring.")
        return render(request, "registrator/verify_login_sms.html", {"phone": user_phone})

    return redirect("login")


def logout_view(request):
    logout(request)  # Django's logout() function
    return redirect("login")

@login_required
def profile(request):
    return render(request, "registrator/profile.html", {"user": request.user})




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

    context = {
        "product_categorys":product_categorys,
        "new_products":new_products,
        "discount_products":discount_products,
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
        products = Products.objects.filter(productcategory_id__in=all_category_ids).order_by('-id')
    else:
        products = Products.objects.all().order_by('-id')  # Agar kategoriya tanlanmasa, barcha mahsulotlarni chiqaramiz


    paginator = Paginator(products, 20)  # Har bir sahifada 5 ta yangilik
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



def checkout(request):
    if request.method == "POST":
        user = request.user
        address = request.POST.get("address")
        product_ids = request.POST.getlist("products")  # CheckBox yoki JSON orqali keladi
        total_price = sum([Products.objects.get(id=pid).price for pid in product_ids])

        order = Order.objects.create(user=user, address=address, total_price=total_price)
        order.products.set(Products.objects.filter(id__in=product_ids))

        # SMS kod yaratish
        verification_code = random.randint(1000, 9999)
        request.session["order_verification_code"] = verification_code
        send_sms(user.phone, verification_code)
        print(verification_code)

        return redirect("confirm_order")

    return render(request, "checkout.html")

def confirm_order(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        verification_code = request.session.get("order_verification_code")

        if int(entered_code) == verification_code:
            order = Order.objects.filter(user=request.user, status="pending").last()
            order.status = "confirmed"
            order.save()
            return redirect("order_success")

        return render(request, "confirm_order.html", {"error": "Kod noto‘g‘ri!"})

    return render(request, "confirm_order.html")
