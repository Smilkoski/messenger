"""chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from messenger import settings
from .views import (
    UserGroupViewSet,
    MessageViewSet,
    GroupViewSet,
)
from .views import (
    index,
    messages,
    new_group,
    add_message,
    update_group,
)

router = routers.DefaultRouter()

router.register(r'user_groups', UserGroupViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path("", index, name="index"),
    path('', include(router.urls)),

    path("new_group/", new_group, name="new_group"),
    path("update_group/<int:group_id>/", update_group, name="update_group"),

]
# API Routes
# path('messages/<int:group_id>/', messages, name='messages'),
# path('add_message/', add_message, name='add_message'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
