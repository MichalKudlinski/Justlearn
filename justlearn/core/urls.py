from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('Student', views.StudentProfileViewSet)

urlpatterns = [
    path('',include(router.urls))
    
]