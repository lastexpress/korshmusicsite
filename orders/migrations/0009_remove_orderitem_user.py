# Generated by Django 3.2.9 on 2022-05-06 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]