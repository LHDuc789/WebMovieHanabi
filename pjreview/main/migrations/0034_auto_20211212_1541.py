# Generated by Django 3.2.8 on 2021-12-12 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_rename_name_typeproduct_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typeproduct',
            name='types',
        ),
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
    ]
