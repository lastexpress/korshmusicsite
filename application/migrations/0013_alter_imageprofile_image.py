# Generated by Django 3.2.9 on 2022-05-02 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_auto_20220502_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
