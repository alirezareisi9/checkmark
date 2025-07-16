from .serializers import UserInfoDetailsSerializer, UserInfoListSerializer
from .models import UserInfo
from .permissions import IsManagerOrReadOnly
from checkmark1.detail_viewset import DetailModelViewSet
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
import operator
from functools import reduce
import random


class UserInfoViewSet(DetailModelViewSet) :

    serializer_class = UserInfoListSerializer
    # If our action is list so serializer_class is UserInfoListSerializer, else it is UserInfoDetailsSerializer
    details_serializer_class = UserInfoDetailsSerializer
    permission_classes = [IsManagerOrReadOnly]


    def get_serializer_class(self):
        if self.action != 'list' and self.details_serializer_class is not None :
            return self.details_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.role == 'MANAGER' :
            # Set multiple querysets on a list
            q_list = [Q(id=self.request.user.id), Q(manager=self.request.user)]
            # Combine two parameters for a queryset by using reduce method
            return UserInfo.objects.filter(reduce(operator.or_, q_list))
        if self.request.user.role == 'REPORTER' :
            return UserInfo.objects.all()
        if self.request.user.role == 'EMPLOYEE' :
            return UserInfo.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        # Give response from create method of Mixin views
        data =  super().create(request, *args, **kwargs)
        # Give object from model
        current_user  = UserInfo.objects.get(pk=data.data['id'])
        # Give random password to password table of data and hash it at last
        random_password = str(random.randint(10000000, 99999999))
        data.data['password'] = random_password
        current_user.set_password(random_password)
        # Save object on db
        current_user.save()
        return data
