# Generated by Django 2.2.7 on 2019-11-25 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('year', models.DateField()),
                ('url', models.URLField()),
                ('categories', models.ManyToManyField(to='films.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False)),
                ('age', models.PositiveSmallIntegerField()),
                ('sex', models.CharField(choices=[('M', 'Man'), ('F', 'Femme')], max_length=5)),
                ('postal_code', models.CharField(max_length=500)),
                ('occupation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.Occupation')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField()),
                ('categories', models.ManyToManyField(to='films.Category')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.Film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.User')),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='rating',
            field=models.ManyToManyField(through='films.Rate', to='films.User'),
        ),
    ]
