# lib
# third-party
from rest_framework import serializers
# local
from .models import CustomUser
from .models import CustomUser




# List of instances of UserInfo : List serializer of user route
class UserListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'role'
        ]


class UserCreateSerializer(serializers.HyperlinkedModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'username', 
            'password', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'national_code', 
            'employee_code', 
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'role', 
            'manager', 
            'change_password', 
            'leave_limit'
        ]

    password = serializers.CharField(write_only=True)



# Detail of any instance of UserInfo : Detail serializer of user route
class UserDetailSerializer(serializers.HyperlinkedModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'national_code', 
            'employee_code', 
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'role', 
            'manager', 
            'change_password', 
            'leave_limit'
        ]

    manager = serializers.HyperlinkedRelatedField(
        view_name='user-detail', 
        read_only=True
    )
