# Generated by Django 2.0.5 on 2018-07-08 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_auto_20180708_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='slug',
        ),
    ]