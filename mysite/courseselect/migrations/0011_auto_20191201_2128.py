# Generated by Django 2.1.8 on 2019-12-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseselect', '0010_pre_is_loved'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_time',
            field=models.IntegerField(default=0, verbose_name='结束节'),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_week',
            field=models.IntegerField(default=1, verbose_name='开始周次'),
        ),
    ]
