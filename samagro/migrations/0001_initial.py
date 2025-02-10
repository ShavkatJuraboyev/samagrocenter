# Generated by Django 5.1.6 on 2025-02-09 05:23

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/img/', verbose_name='Rasm')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Rasm',
                'verbose_name_plural': 'Rasmlar',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(default='Familiyasi', max_length=100, verbose_name='Foydalanuvchi ismi')),
                ('last_name', models.CharField(default='Familiyasi', max_length=100, verbose_name='Foydalanuvchi familiyasi')),
                ('phone', models.CharField(max_length=13, unique=True, verbose_name='Telefon raqami')),
                ('is_active', models.BooleanField(default=False, verbose_name='Tasdiqlanganmi?')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Adminmi?')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/category/', verbose_name='Maxsulot kategoriyasi rasmi')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='Maxsulot kategoryasi nomi')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='samagro.productcategory', verbose_name='Ota Kategoriya')),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Maxsulot kategoriyasi',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Maxsulot nomi')),
                ('price', models.CharField(blank=True, max_length=50, null=True, verbose_name='Maxsulot narxi')),
                ('text', models.TextField(blank=True, null=True, verbose_name="Maxsulot haqida ma'lumot")),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name="Maxsulot haqida umumiy ma'lumot")),
                ('is_discount', models.BooleanField(blank=True, default=False, null=True, verbose_name='Chegirma berish')),
                ('price_discount', models.CharField(blank=True, max_length=50, null=True, verbose_name='Maxsulot chegirma narxi')),
                ('date_end_discount', models.DateField(blank=True, null=True, verbose_name='Chegrima tugash vaqti')),
                ('percent_discount', models.CharField(blank=True, max_length=4, null=True, verbose_name='Chegirma foizi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='O‘zgartirilgan vaqt')),
                ('images', models.ManyToManyField(blank=True, to='samagro.productpicture', verbose_name='Maxsulot rasmlari')),
                ('productcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='samagro.productcategory', verbose_name='Maxsulot turi')),
            ],
            options={
                'verbose_name': 'Maxsulot',
                'verbose_name_plural': 'Maxsulotlar',
            },
        ),
    ]
