# Generated by Django 2.0 on 2020-05-16 15:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20200513_2017'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0002_auto_20200506_1432'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shopcart',
            unique_together={('user', 'goods')},
        ),
    ]
