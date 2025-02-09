from django.db import models
from django.templatetags.static import static
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

# Foydalanuvchi Manageri
class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None):
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart")
        user = self.model(phone=phone, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = False  # Foydalanuvchi tasdiqlanmagan
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password=None):
        user = self.create_user(phone, first_name, last_name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True  # Django superuser bo'lishi uchun
        user.is_active = True
        user.save(using=self._db)
        return user

# Foydalanuvchi modeli
class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="Foydalanuvchi ismi", default="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Foydalanuvchi familiyasi", default="Familiyasi")
    phone = models.CharField(max_length=13, unique=True, verbose_name="Telefon raqami")

    is_active = models.BooleanField(default=False, verbose_name="Tasdiqlanganmi?")
    is_admin = models.BooleanField(default=False, verbose_name="Adminmi?")
    is_staff = models.BooleanField(default=False)  # Django admin paneli uchun
    is_superuser = models.BooleanField(default=False)  # Django superuser uchun

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  # Django'ning default user modeli bilan to‘qnashuvni oldini oladi
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  # Django'ning default user modeli bilan to‘qnashuvni oldini oladi
        blank=True,
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class ProductCategory(models.Model):
    image = models.ImageField(upload_to='product/category/', null=True, blank=True, verbose_name="Maxsulot kategoriyasi rasmi")
    name = models.CharField(max_length=50, null=True, verbose_name="Maxsulot kategoryasi nomi")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name="Ota Kategoriya" )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Maxsulot kategoriyasi"

    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = ProductCategory.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=True)

        except ProductCategory.DoesNotExist:
            pass
        super(ProductCategory, self).save(*args, **kwargs)

    def get_produc_category_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('assets/images/category.png')
    
class ProductPicture(models.Model):
    image = models.ImageField(upload_to='product/img/', verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rasm {self.id}"
    
    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"

    def get_produc_img(self):
        # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
        return self.image.url if self.image else static('assets/images/product.png')
    
class Products(models.Model):
    productcategory = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Maxsulot turi")
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Maxsulot nomi")
    images = models.ManyToManyField(ProductPicture, blank=True, verbose_name="Maxsulot rasmlari")
    price = models.CharField(max_length=50, null=True, blank=True, verbose_name="Maxsulot narxi")
    text = models.TextField(null=True, blank=True, verbose_name="Maxsulot haqida ma'lumot")
    content = RichTextUploadingField(config_name='extends', verbose_name="Maxsulot haqida umumiy ma'lumot", null=True, blank=True)

    is_discount = models.BooleanField(default=False, null=True, blank=True, verbose_name="Chegirma berish")
    price_discount = models.CharField(max_length=50, null=True, blank=True, verbose_name="Maxsulot chegirma narxi")
    date_end_discount = models.DateField(null=True, blank=True, verbose_name="Chegrima tugash vaqti")
    percent_discount = models.CharField(max_length=4, null=True, blank=True, verbose_name="Chegirma foizi")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O‘zgartirilgan vaqt")

    class Meta:
            verbose_name = "Maxsulot"
            verbose_name_plural = "Maxsulotlar"


    def __str__(self):
            return self.name


# Buyurtma modeli
class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    products = models.ManyToManyField("Products", verbose_name="Maxsulotlar")
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Ko'cha manzili")
    state = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ko'cha nomi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jami narx")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Kutish"), ("confirmed", "Tasdiqlangan"), ("shipped", "Jo‘natilgan")],
        default="pending",
        verbose_name="Holati",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return f"Buyurtma {self.id} - {self.user.phone}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"



class News(models.Model):
    image = models.ImageField(upload_to='news/images/', null=True, blank=True, verbose_name="Sarlovha rasmi")
    title = models.CharField(max_length=200, null=True, help_text="Sarlavha maksimal 200 belgi", verbose_name="Sarlovhasi")
    text = models.CharField(max_length=500, null=True, help_text="Sarlavha matini maksimal 500 belgi", verbose_name="Sarlovha matini")
    content = RichTextUploadingField(config_name='extends', verbose_name="Sarlovha umumiy matini", null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, default=now)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def get_post_img(self):
        return self.image.url if self.image else static('')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = News.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.image and this.image != self.image:
                this.image.delete(save=True)
        except News.DoesNotExist:
            pass
        super(News, self).save(*args, **kwargs)