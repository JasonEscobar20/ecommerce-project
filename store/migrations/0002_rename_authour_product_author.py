# Generated by Django 4.2 on 2023-04-03 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='authour',
            new_name='author',
        ),
    ]
