from .models import UserInfo
from rest_framework import serializers
from .models import UserInfo




# List of instances of UserInfo : List serializer of user route
class UserInfoListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = UserInfo
        fields = [
            'id', 'username', 'first_name', 'last_name', 'role'
        ]

# Detail of any instance of UserInfo : Detail serializer of user route
class UserInfoDetailsSerializer(serializers.ModelSerializer) :
    class Meta :
        model = UserInfo
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'national_code', 
            'employee_code', 'is_active', 'is_staff', 'is_superuser', 'role', 'manager', 'change_password', 'leave_limit'
        ]

    password = serializers.CharField(read_only=True)  # its not on Meta block


        # read_only_fields=['password']  # If make field read_only, can't access and modify it

