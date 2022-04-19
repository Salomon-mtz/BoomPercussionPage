from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=20)
    # username = models.CharField(max_length=20)
    # email = models.CharField(max_length=30)
    # password = models.CharField(max_length=20)
    level = models.CharField(max_length=1)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.player.save()
    
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
    score = models.IntegerField()
    attemps = models.IntegerField()
    timeToSolve = models.IntegerField()
    level = models.IntegerField()
    

class Global(models.Model):
    username = models.CharField(max_length=20)
    globalScore = models.IntegerField()
    timeFinish = models.IntegerField()
    timePlayed = models.IntegerField()
    level = models.IntegerField()