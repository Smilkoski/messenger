from datetime import datetime

from django.db import models

from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50, default='')

    def serializable(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description, }


class Message(models.Model):
    message = models.CharField(max_length=140)
    date = models.DateTimeField(default=datetime.now)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_custom_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='message_group')

    def serializable(self):
        return {'id': self.id,
                'message': self.message,
                'date': self.date,
                'custom_user': self.custom_user.user.username,
                'custom_user_id': self.custom_user.id,
                'custom_user_image_url': self.custom_user.image.url,
                'group': self.group.serializable(), }
