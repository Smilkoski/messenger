# Generated by Django 3.2 on 2022-01-09 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_newuser_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='biography',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='C:/Users/Hristijan/PycharmProjects/messenger/media/default.jpg', upload_to='C:/Users/Hristijan/PycharmProjects/messenger/media/profile_pics'),
        ),
    ]
