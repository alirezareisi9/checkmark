# lib
# third-party
from rest_framework import serializers
# local
from .models import CustomUser
from .models import CustomUser




# List of instances of Users : List serializer of user route
class UserListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'employee_code', 
            'first_name', 
            'last_name', 
            'role'
        ]


class UserCreateSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'employee_code', 
            'password', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'national_code', 
            'role', 
            'manager', 
            'change_password', 
            'leave_limit',
            'is_active', 
            'is_staff', 
            'is_superuser', 
        ]

    password = serializers.CharField(read_only=True)



# Detail of any instance of Users : Detail serializer of user route
class UserDetailSerializer(serializers.HyperlinkedModelSerializer) :
    
    manager = serializers.HyperlinkedRelatedField(
        view_name='authentication:users-detail',
        read_only=True
    )
    # Relational field must provide a `queryset` argument, override `get_queryset`, or set read_only=`True`
    
    class Meta :
        model = CustomUser
        fields = [
            'id', 
            'employee_code', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'national_code', 
            'role', 
            'manager', 
            'change_password', 
            'leave_limit', 
            'is_active', 
            'is_staff', 
            'is_superuser', 
        ]



class ChangePasswordSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8, 
        style={'input_type': 'password'},
    )
