from django.shortcuts import get_object_or_404 , render
from .models import *
from rest_framework.views import APIView
from rest_framework.mixins import *
from rest_framework import generics
from django.contrib import messages
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
import time
import datetime
from ..authentication.models import * 
from ..authentication.serializers import *


class FingerLog(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    
    def get_serializer_class(self):
        return UserSerializer
    
    
    @action(detail=False, methods=['get']) # POST

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        target_queryset = Log.objects.all()
        
        target = Log.objects.filter(user__username__iexact=serializer.data["username"] , exit=None , date=datetime.datetime.now())
        print(target)
        if len(target) != 0:
            for targets in target:
                targets.exit = datetime.datetime.now()
                targets.save()
                return Response("true")
        else:
            user = CustomUser.objects.filter(username=serializer.data["username"])
            for users in user:
                target = Log(user=users , date=time.strftime("%Y-%m-%d" , time.localtime()) , enterance=datetime.datetime.now() , text="auto added")
                target.save()
                return Response("meow!!")
        return Response("mewo meow")


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    #make sure to make manager perms after getting manager and user 