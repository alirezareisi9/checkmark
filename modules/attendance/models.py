from django.db import models
from django.contrib.auth.models import User
from ..authentication.models import * 
from ..authentication.serializers import *
class Log(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE) 
    
    # TODO: Manager *********** 
    exit = models.TimeField(null=True)
    enterance = models.TimeField()
    approved_by = models.ForeignKey("authentication.CustomUser", max_length=70, on_delete=models.CASCADE, related_name="user_logs" , default=1)
    text = models.TextField()
    date = models.DateField(auto_created=True)
    
    def __str__(self) -> str:
        return self.user.username 




