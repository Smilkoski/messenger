from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomUser
from .models import (
    Group,
    Message,
    UserGroup
)


def index(request):
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


def new_group(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['description']
        # g = Group(name=name,description=desc)
        # g.save()

        names = [c.user.username for c in list(CustomUser.objects.all())]
        names_to_add = []
        for name in names:
            if request.POST[names] is not None:
                names_to_add.append(name)

        print(request)

    else:
        context = {}
        context['custom_users'] = CustomUser.objects.all()
        return render(request, 'chat/new_group.html', context)
