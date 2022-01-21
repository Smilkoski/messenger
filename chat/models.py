from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User, Group
from django.db import models


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    biography = models.TextField(default='')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Message(models.Model):
    message = models.CharField(max_length=140)
    date = models.DateTimeField(default=datetime.now)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_custom_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='message_group')


class UserGroup(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='custom_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
