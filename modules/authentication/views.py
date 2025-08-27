# lib
import random
# third-party
from django.db.models import Q
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import UpdateAPIView
# local
from checkmark1.detail_viewset import DetailModelViewSet

from .serializers import (UserDetailSerializer,
                           UserListSerializer, 
                           UserCreateSerializer, 
                           ChangePasswordSerializer)

from .models import CustomUser
from .permissions import IsManagerOrReadOnly



class CustomUserPagination(PageNumberPagination):
    page_size = 10  # Default num of items per page
    page_size_query_param = 'page-size'  # Name of query parameter shown
    # num of items per page
    max_page_size = 50  # Max items user can selected to show per page



class UsersViewSet(DetailModelViewSet) :

    # If our action is list so serializer_class is UserListSerializer,
    #  if it's create so UserCreateSerializer else it is UserDetailsSerializer
    serializer_class = UserListSerializer
    details_serializer_class = UserDetailSerializer
    create_serializer_class = UserCreateSerializer

    pagination_class = CustomUserPagination

    permission_classes = [IsManagerOrReadOnly,]



    def get_serializer_class(self):
        
        if self.action == 'create' and self.create_serializer_class:
            return self.create_serializer_class
        
        return super().get_serializer_class()



    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['request'] = self.request
        return context



    def get_queryset(self):
        user = self.request.user

        if user.role == 'MANAGER' :
            return CustomUser.objects.filter(Q(id=user.id) | Q(manager=user))
        
        elif user.role == 'REPORTER' :
            return CustomUser.objects.all()
        
        elif user.role == 'EMPLOYEE' :
            return CustomUser.objects.filter(id=user.id)

        return CustomUser.objects.none()



    def create(self, request, *args, **kwargs):
        # Give response from create method of Mixin views
        data =  super().create(request, *args, **kwargs)
        
        current_user  = CustomUser.objects.get(pk=data.data['id'])

        random_password = str(random.randint(10000000, 99999999))
        current_user.set_password(random_password)
        # Save object on db
        current_user.save()

        data.data['password'] = random_password
        return data



class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user