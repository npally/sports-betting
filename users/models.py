from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    favorite_team = models.CharField(max_length=100)
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    
    def __str__(self):
        return self.username

    def get_name(self):
        return self.first_name + " " + self.last_name
