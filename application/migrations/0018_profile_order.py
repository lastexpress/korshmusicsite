# Generated by Django 3.2.9 on 2022-05-06 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_orderitem_user'),
        ('application', '0017_auto_20220502_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]