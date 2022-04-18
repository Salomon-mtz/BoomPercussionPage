from unicodedata import name
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    level = models.CharField(max_length=1)
    
    def toJson(self):
        a = {
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'level': self.level
            
        }
        return a


class Plays(models.Model):
    username = models.CharField(max_length=20)
    score = models.IntegerField(max_length=30)
    attemps = models.IntegerField(max_length=20)
    timeToSolve = models.IntegerField(max_length=20)
    level = models.IntegerField(max_length=1)
    

class Global(models.Model):
    username = models.CharField(max_length=20)
    globalScore = models.IntegerField(max_length=30)
    timeFinish = models.IntegerField(max_length=20)
    timePlayed = models.IntegerField(max_length=20)
    level = models.IntegerField(max_length=1)