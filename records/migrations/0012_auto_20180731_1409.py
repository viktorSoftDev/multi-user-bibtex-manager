# Generated by Django 2.0.5 on 2018-07-31 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0011_record_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='projects.Project'),
        ),
    ]
