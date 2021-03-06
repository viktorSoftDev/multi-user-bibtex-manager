# Generated by Django 2.0.5 on 2018-07-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20180629_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='entry_type',
            field=models.CharField(choices=[(1, 'article'), (2, 'book'), (3, 'booklet'), (4, 'conference'), (5, 'inbook'), (6, 'incollections'), (7, 'inproceedings'), (8, 'manual'), (9, 'mastersthesis'), (10, 'misc'), (11, 'phdthesis'), (12, 'proceedings'), (13, 'techreport'), (14, 'unpublished')], max_length=64),
        ),
    ]
