# Generated by Django 2.2.7 on 2020-01-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='city',
            field=models.TextField(default='City'),
        ),
        migrations.AddField(
            model_name='offer',
            name='country',
            field=models.TextField(default='Country'),
        ),
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(default='Description'),
        ),
        migrations.AddField(
            model_name='offer',
            name='enterprise',
            field=models.TextField(default='Enterprise'),
        ),
        migrations.AddField(
            model_name='offer',
            name='immediate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='months',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='offer',
            name='province',
            field=models.TextField(default='Province'),
        ),
        migrations.AddField(
            model_name='offer',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='offer',
            name='university',
            field=models.TextField(default='University'),
        ),
    ]