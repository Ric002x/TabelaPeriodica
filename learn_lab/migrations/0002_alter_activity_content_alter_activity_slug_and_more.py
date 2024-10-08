# Generated by Django 5.1.1 on 2024-09-08 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='content',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
