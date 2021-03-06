# Generated by Django 2.0.5 on 2018-07-09 13:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_remove_record_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='address',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='author',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='booktitle',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='chapter',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='cite_key',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='doi',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='edition',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='editor',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='how_published',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='institution',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='isbn',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='issn',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='journal',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='last_edited',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='record',
            name='month',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='note',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='organisation',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='pages',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='record',
            name='publisher',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='school',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='series',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='subtitle',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='title',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='type',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='urldate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='volume',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
