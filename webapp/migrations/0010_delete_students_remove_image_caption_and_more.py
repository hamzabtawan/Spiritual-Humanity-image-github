# Generated by Django 4.0.3 on 2022-11-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_students_alter_image_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Students',
        ),
        migrations.RemoveField(
            model_name='image',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='caption',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=False, upload_to='img/%y'),
        ),
    ]
