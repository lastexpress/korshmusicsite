# Generated by Django 3.2.9 on 2022-02-28 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_alter_album_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата релиза'),
        ),
    ]
