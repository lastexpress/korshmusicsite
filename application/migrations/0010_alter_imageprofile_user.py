# Generated by Django 3.2.9 on 2022-05-02 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_imageprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.profile'),
        ),
    ]
