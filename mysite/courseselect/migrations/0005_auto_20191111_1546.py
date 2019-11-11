# Generated by Django 2.1.8 on 2019-11-11 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseselect', '0004_auto_20191108_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentcourse',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentcourse',
            name='student',
        ),
        migrations.AlterField(
            model_name='student',
            name='s_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='学号'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='t_id',
            field=models.AutoField(max_length=20, primary_key=True, serialize=False, verbose_name='工号'),
        ),
        migrations.DeleteModel(
            name='StudentCourse',
        ),
    ]