# Generated by Django 4.0.3 on 2022-04-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boomSite', '0002_remove_player_email_remove_player_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.CharField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='password',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='username',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
