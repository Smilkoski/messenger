from rest_framework import serializers

from .models import (
    Group,
    Message,
    UserGroup,
)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'description')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message', 'date', 'custom_user', 'group')


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('custom_user', 'group')
