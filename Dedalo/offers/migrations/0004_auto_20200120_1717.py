# Generated by Django 2.2.7 on 2020-01-20 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_auto_20200117_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='country',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='enterprise',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='immediate',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='province',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='university',
            field=models.TextField(blank=True, null=True),
        ),
    ]