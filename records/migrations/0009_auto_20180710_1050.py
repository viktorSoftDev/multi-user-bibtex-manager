# Generated by Django 2.0.5 on 2018-07-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_auto_20180710_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='entry_type',
            field=models.CharField(choices=[('article', 'article'), ('book', 'book'), ('booklet', 'booklet'), ('conference', 'conference'), ('inbook', 'inbook'), ('incollections', 'incollections'), ('inproceedings', 'inproceedings'), ('manual', 'manual'), ('mastersthesis', 'mastersthesis'), ('misc', 'misc'), ('phdthesis', 'phdthesis'), ('proceedings', 'proceedings'), ('techreport', 'techreport'), ('unpublished', 'unpublished')], default='Please Select', max_length=64),
        ),
    ]
