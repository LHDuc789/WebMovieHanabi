# Generated by Django 3.2.8 on 2021-12-06 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_product_product_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cast',
            field=models.CharField(blank=True, max_length=800, null=True, verbose_name='Diễn Viên Nổi Bật'),
        ),
    ]
