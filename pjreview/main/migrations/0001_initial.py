# Generated by Django 3.2.8 on 2021-11-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('director', models.CharField(max_length=300)),
                ('cast', models.CharField(max_length=800)),
                ('description', models.TextField(max_length=5000)),
                ('release_date', models.DateField()),
                ('averageRating', models.FloatField()),
            ],
        ),
    ]
