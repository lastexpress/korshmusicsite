# Generated by Django 3.2.9 on 2022-05-02 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_auto_20220502_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image_prof/group/', verbose_name='Аватарка'),
        ),
        migrations.DeleteModel(
            name='ImageProfile',
        ),
    ]
