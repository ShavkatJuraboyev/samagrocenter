# Generated by Django 5.1.6 on 2025-02-09 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('samagro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(default='Ismi', max_length=100, verbose_name='Foydalanuvchi ismi'),
        ),
    ]
