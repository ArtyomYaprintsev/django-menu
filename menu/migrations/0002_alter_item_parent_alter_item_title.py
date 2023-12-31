# Generated by Django 5.0 on 2023-12-07 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, help_text='TODO: add help text.', null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.item', verbose_name='parent item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=25, verbose_name='title'),
        ),
    ]
