# Generated by Django 2.0 on 2020-05-13 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_hotsearchwords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='desc',
            new_name='goods_desc',
        ),
    ]