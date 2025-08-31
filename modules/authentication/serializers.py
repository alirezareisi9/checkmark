# lib
# third-party
from django.contrib.auth import password_validation
from rest_framework import serializers
# local
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

        read_only_fields = [
            'id',
            'password',
            'manager',
            'change_password',
            'is_active', 
            'is_staff', 
            'is_superuser',
        ]
    



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

        read_only_fields = [
            'id',
            'manager',
            'change_password',
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


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(  # PATCH doesn't care it's required and initialize it to None
        required=True, 
        write_only=True,
        min_length=8, 
        style={'input_type': 'password'},
    )
    class Meta:
        model = CustomUser
        fields = [
            'password'
        ]


    def update(self, instance, validated_data):
        
        password = validated_data.get('password')
        
        password_validation.validate_password(password, user=instance)
        
        instance.set_password(password)
        instance.change_password = True
        instance.save()

        return instance