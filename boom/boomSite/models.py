from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default=0)
    first_name = models.CharField(max_length=20, default=0)
    username = models.CharField(max_length=20, default=0)
    email = models.CharField(max_length=30, default=0)
    password = models.CharField(max_length=20, default=0)
    level = models.IntegerField(default=1)
    country = models.CharField(max_length=50, default=0)
    
    @receiver(post_save, sender=User)
    def create_user_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_player(sender, instance, **kwargs):
        instance.player.save()
    
    def toJson(self):
        a = {
            'name': self.first_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'level': self.level,
            'country': self.country
            
        }
        return a


class Plays(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    score = models.IntegerField()
    attempts = models.IntegerField()
    timeToSolve = models.DecimalField(max_digits=5, decimal_places=2)
    level = models.IntegerField()
    

class Global(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    globalScore = models.IntegerField()
    timeFinish = models.DecimalField(max_digits=5, decimal_places=2)
    timePlayed = models.DecimalField(max_digits=5, decimal_places=2)
    level = models.IntegerField()
    
    # def __init__(id, username, globalScore, timeFinish, timePlayed, level) -> None:
    #     super().__init__(id, username, globalScore, timeFinish, timePlayed, level)
