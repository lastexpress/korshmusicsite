# Generated by Django 3.2.9 on 2022-03-05 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-publish',)},
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='publish_date',
            new_name='publish',
        ),
    ]
