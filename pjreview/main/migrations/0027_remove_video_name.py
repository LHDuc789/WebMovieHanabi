# Generated by Django 3.2.8 on 2021-12-10 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20211210_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
    ]
