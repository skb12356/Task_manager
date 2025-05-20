from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    mobile_no = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"