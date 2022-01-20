import json
import random
import string

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from rest_framework import viewsets

from serializers import (
    GroupSerializer,
    UserGroupSerializer,
    MessageSerializer,
)
from users.models import CustomUser
from .models import (
    Group,
    Message,
    UserGroup,
)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer


@ratelimit(key='ip', rate='100/d', block=True)
def index(request):
    if request.user.is_anonymous:
        return redirect(reverse('login'))

    # get groups where current user is present
    usergroups = UserGroup.objects \
        .filter(custom_user__user__username=request.user).all()
    groups = Group.objects.filter(group__in=usergroups)

    context = {
        'groups': groups,
    }
    return render(request, 'chat/index.html', context)


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def messages(request, group_id):
    # Query for requested message
    try:
        g = Group.objects.get(id=group_id)
        messages = Message.objects.filter(group=g).all().order_by('-date')
    except Message.DoesNotExist:
        return JsonResponse({"error": "Messages not found."}, status=404)

    if messages is not None:
        messages = [m.serializable() for m in list(messages)]
        return JsonResponse({i: messages[i] for i in range(len(messages))})

    else:
        return JsonResponse({
            "error": "ERROR"
        }, status=400)


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def new_group(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['description']
        if Group.objects.filter(name=name).exists():
            name += '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        g = Group.objects.create(name=name, description=desc)
        g.save()

        names = list(request.POST)[3:]
        customusers = CustomUser.objects.filter(user__username__in=names).all()
        for cu in customusers:
            ug = UserGroup(custom_user=cu, group=g)
            ug.save()

        current_user = CustomUser.objects.get(user_id=request.user.id)
        ug = UserGroup(custom_user=current_user, group=g)
        ug.save()

        return redirect(reverse('index'))
    else:
        context = {
            'custom_users': CustomUser.objects.all()
        }
        return render(request, 'chat/new_group.html', context)


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def add_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    message = Message(custom_user_id=data['user_id'], group_id=data['group_id'], message=data['msg'])
    message.save()

    return JsonResponse({"message": "Message saved successfully."}, status=201)


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def update_group(request, group_id):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['description']

        UserGroup.objects.filter(group_id=group_id).delete()

        Group.objects.filter(id=group_id).update(name=name, description=desc)
        g = Group.objects.get(id=group_id)
        names = list(request.POST)[3:]
        custom_users = CustomUser.objects.filter(user__username__in=names).all()
        for cu in custom_users:
            ug = UserGroup(custom_user=cu, group=g)
            ug.save()

        return redirect(reverse('index'))

    else:
        participants = UserGroup.objects.filter(group_id=group_id).all().values_list('custom_user', flat=True)
        participants_ids = tuple(participants)
        participants = CustomUser.objects.filter(user_id__in=participants_ids).all()

        not_participants = CustomUser.objects.raw(
            f'select id,user_id from users_customuser WHERE user_id NOT IN {participants_ids}')

        g = Group.objects.get(id=group_id)
        context = {
            'group_id': group_id,
            'group_name': g.name,
            'group_desc': g.description,
            'participants': participants,
            'not_participants': not_participants,
        }

        return render(request, 'chat/update_group.html', context)
