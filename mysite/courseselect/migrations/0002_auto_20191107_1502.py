# Generated by Django 2.1.8 on 2019-11-07 07:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courseselect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('d_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': '院系',
            },
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['pub_date', 'department'], 'verbose_name': '课程'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '学生'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '教师'},
        ),
        migrations.AlterField(
            model_name='course',
            name='c_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='课程id'),
        ),
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseselect.Department', verbose_name='所属院系'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=40, verbose_name='课程名称'),
        ),
        migrations.AlterField(
            model_name='course',
            name='pub_date',
            field=models.DateField(verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=20, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='t_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='工号'),
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='courseselect.Department', verbose_name='所属院系'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(default=datetime.datetime(2019, 11, 7, 7, 2, 30, 639948, tzinfo=utc), on_delete=django.db.models.deletion.CASCADE, to='courseselect.Department', verbose_name='所属院系'),
            preserve_default=False,
        ),
    ]
