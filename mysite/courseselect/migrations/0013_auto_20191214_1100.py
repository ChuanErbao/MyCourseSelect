# Generated by Django 2.1.8 on 2019-12-14 03:00

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('courseselect', '0012_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=tinymce.models.HTMLField(verbose_name='正文'),
        ),
    ]