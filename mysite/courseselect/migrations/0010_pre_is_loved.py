# Generated by Django 2.1.8 on 2019-12-01 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseselect', '0009_auto_20191201_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='pre',
            name='is_loved',
            field=models.CharField(choices=[('is', 'is'), ('not', 'not')], default='not', max_length=10, verbose_name='是否收藏'),
        ),
    ]