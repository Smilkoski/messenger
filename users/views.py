import string
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

from .models import CustomUser


@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def profile(request, id):
    user = CustomUser.objects.get(id=id)
    context = {'user': user}

    return render(request, 'users/profile.html', context)


@ratelimit(key='ip', rate='100/d', block=True)
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def validate_password_strength(value):
    if len(value) < 10:
        return False

    # check for digit
    if not any(char.isdigit() for char in value):
        return False

    # check for upper letter
    if not any(char.isupper() for char in value):
        return False

    # check for lower letter
    if not any(char.islower() for char in value):
        return False

    # check for special character
    if not any(char.intersection(string.punctuation) for char in value):
        return False

    return True


@ratelimit(key='ip', rate='100/d', block=True)
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image = request.POST['img']

        # Ensure password matches confirmation
        password = request.POST["password"]
        # password must have special characters, numbers, upper and lower letters
        if not validate_password_strength(password):
            messages.error(request, 'Password must have special characters, numbers, upper and lower letters')
            return render(request, "users/register.html",)

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            cu = CustomUser(user=user, image=image)
            cu.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html")


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='100/d', block=True)
def user(request, user_id):
    # Query for requested message
    try:
        custom_user = CustomUser.objects.get(user_id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if custom_user is not None:
        return JsonResponse(custom_user.serializable())

    else:
        return JsonResponse({
            "error": "ERROR"
        }, status=400)
