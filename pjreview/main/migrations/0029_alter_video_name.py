# Generated by Django 3.2.8 on 2021-12-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_video_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]