# Generated by Django 3.2.9 on 2022-04-22 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_name',
        ),
    ]
