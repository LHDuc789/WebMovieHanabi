# Generated by Django 3.2.8 on 2021-11-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_product_averagerating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.URLField(default=None, null=True, verbose_name='Trailer'),
        ),
    ]
