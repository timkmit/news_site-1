# Generated by Django 3.2.7 on 2022-02-13 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_auto_20220213_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='like',
        ),
    ]
