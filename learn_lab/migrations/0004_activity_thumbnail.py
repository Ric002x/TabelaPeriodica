# Generated by Django 5.1.1 on 2024-09-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_lab', '0003_alter_activity_file_alter_activity_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='thumbnail',
            field=models.ImageField(blank=True, default='', upload_to='learn_lab/thumbnails/'),
        ),
    ]
