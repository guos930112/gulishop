# Generated by Django 2.0 on 2020-05-13 21:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0004_auto_20200513_2017'),
        ('operations', '0002_auto_20200506_1432'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together={('user', 'goods')},
        ),
    ]
