from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [ "id","user" , "text" , "approved_by" , "exit" , "enterance" , "date"]
        #make sure to make a require field in exit
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ["id" ,"user"]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username"]
    username = serializers.CharField(max_length=90)
    def validate_username(self, value):
        return value