from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Group,
    Message
)


def index(request):
    context = {
        'groups': Group.objects.all()
    }
    return render(request, 'chat/index.html', context)


@csrf_exempt
@login_required
def messages(request, group_id):
    # Query for requested message
    try:
        g = Group.objects.get(id=group_id)
        messages = Message.objects.filter(group=g).all()
    except Message.DoesNotExist:
        return JsonResponse({"error": "Messages not found."}, status=404)

    if messages is not None:
        messages = [m.serializable() for m in list(messages)]
        return JsonResponse({i: messages[i] for i in range(len(messages))})

    else:
        return JsonResponse({
            "error": "ERROR"
        }, status=400)
