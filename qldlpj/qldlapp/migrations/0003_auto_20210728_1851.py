# Generated by Django 3.2.5 on 2021-07-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldlapp', '0002_auto_20210728_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khachhang',
            name='gmail',
            field=models.CharField(default=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='money',
            field=models.CharField(default=True, max_length=9999, null=True),
        ),
        migrations.AlterField(
            model_name='khachhang',
            name='sdt',
            field=models.CharField(default=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='duaration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
