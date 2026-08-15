from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register('person', views.PersonViewSet)
router.register('user', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]