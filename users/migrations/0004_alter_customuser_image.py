# Generated by Django 3.2 on 2022-01-10 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220109_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='media/default.jpg', upload_to='media/profile_pics'),
        ),
    ]
