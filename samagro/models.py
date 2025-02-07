from django.db import models
from django.templatetags.static import static
from ckeditor_uploader.fields import RichTextUploadingField 
# Create your models here.

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
                this.image.delete(save=False)
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
    price = models.FloatField(null=True, blank=True, verbose_name="Maxsulot narxi")
    text = models.TextField(null=True, blank=True, verbose_name="Maxsulot haqida ma'lumot")
    content = RichTextUploadingField(config_name='extends', verbose_name="Maxsulot haqida umumiy ma'lumot", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O‘zgartirilgan vaqt")

    class Meta:
            verbose_name = "Maxsulot"
            verbose_name_plural = "Maxsulotlar"

    def get_produc_img_there(self):
            # Agar rasm mavjud bo'lmasa, static fayldan default rasmni qaytaradi
            return self.image.url if self.image else static('assets/images/product.png')

    def __str__(self):
            return self.name

