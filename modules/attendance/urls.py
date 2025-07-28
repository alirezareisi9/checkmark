from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views


app_name = 'attendance'

router = routers.DefaultRouter()
router.register(prefix='Log' , viewset=views.LogViewSet , basename="Log")



urlpatterns = [
    path('autolog/' , views.FingerLog.as_view(), name='meow'),
] +  router.urls