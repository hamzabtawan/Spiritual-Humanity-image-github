# Generated by Django 4.0.3 on 2022-11-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_rename_name_image_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
