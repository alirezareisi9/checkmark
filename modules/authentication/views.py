# lib
import random
# third-party
from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# local
from checkmark1.detail_viewset import DetailModelViewSet
from .serializers import UserDetailSerializer, UserListSerializer
from .models import CustomUser
from .permissions import IsManagerOrReadOnly



class CustomUserPagination(PageNumberPagination):
    page_size = 10  # Default num of items per page
    page_size_query_param = 'page-size'  # Name of query parameter shown
    # num of items per page
    max_page_size = 50  # Max items user can selected to show per page



class UserInfoViewSet(DetailModelViewSet) :

    # If our action is list so serializer_class is UserInfoListSerializer,
    #  else it is UserInfoDetailsSerializer
    serializer_class = UserListSerializer
    details_serializer_class = UserDetailSerializer

    pagination_class = CustomUserPagination

    permission_classes = [IsManagerOrReadOnly,]


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
        # Give object from model
        current_user  = CustomUser.objects.get(pk=data.data['id'])
        # Give random password to password table of data and hash it at last
        random_password = str(random.randint(10000000, 99999999))
        data.data['password'] = random_password
        current_user.set_password(random_password)
        # Save object on db
        current_user.save()
        return data
