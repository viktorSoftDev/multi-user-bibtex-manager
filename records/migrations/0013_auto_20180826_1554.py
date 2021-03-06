# Generated by Django 2.0.5 on 2018-08-26 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0012_auto_20180731_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='entry_type',
            field=models.CharField(choices=[('', '------------'), ('article', 'article'), ('book', 'book'), ('booklet', 'booklet'), ('conference', 'conference'), ('inbook', 'inbook'), ('incollection', 'incollection'), ('inproceedings', 'inproceedings'), ('manual', 'manual'), ('mastersthesis', 'mastersthesis'), ('misc', 'misc'), ('phdthesis', 'phdthesis'), ('proceedings', 'proceedings'), ('techreport', 'techreport'), ('unpublished', 'unpublished')], max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='last_edited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
