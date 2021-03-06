# Generated by Django 2.0.5 on 2018-07-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20180701_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='slugslug', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='entry_type',
            field=models.CharField(choices=[('article', 'article'), ('book', 'book'), ('booklet', 'booklet'), ('conference', 'conference'), ('inbook', 'inbook'), ('incollections', 'incollections'), ('inproceedings', 'inproceedings'), ('manual', 'manual'), ('mastersthesis', 'mastersthesis'), ('misc', 'misc'), ('phdthesis', 'phdthesis'), ('proceedings', 'proceedings'), ('techreport', 'techreport'), ('unpublished', 'unpublished')], max_length=64),
        ),
    ]
