from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default=0)
    # name = models.CharField(max_length=20)
    # username = models.CharField(max_length=20)
    # email = models.CharField(max_length=30)
    # password = models.CharField(max_length=20)
    level = models.IntegerField(max_length=1, default=1)
    country = models.CharField(max_length=50)
    
    @receiver(post_save, sender=User)
    def create_user_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_player(sender, instance, **kwargs):
        instance.player.save()
    
    def toJson(self):
        a = {
            'name': User.first_name,
            'username': User.username,
            'email': User.email,
            'password': User.password,
            'level': self.level,
            'country': self.country
            
        }
        return a


class Plays(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    score = models.IntegerField()
    attemps = models.IntegerField()
    timeToSolve = models.IntegerField()
    level = models.IntegerField()
    

class Global(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    globalScore = models.IntegerField()
    timeFinish = models.IntegerField()
    timePlayed = models.IntegerField()
    level = models.IntegerField()
    
    # def __init__(id, username, globalScore, timeFinish, timePlayed, level) -> None:
    #     super().__init__(id, username, globalScore, timeFinish, timePlayed, level)
