# Generated by Django 3.2.8 on 2021-12-02 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_delete_watchmovie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='averageRating',
        ),
    ]