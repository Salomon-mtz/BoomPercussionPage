from unicodedata import name
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    gamertag = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20)


