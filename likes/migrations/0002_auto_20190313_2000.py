# Generated by Django 2.0.2 on 2019-03-13 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LikeComment',
            new_name='LikeCount',
        ),
    ]
