from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm
from .forms import NewPlayerForm
import json
from json import dumps, load, loads
from django.views.decorators.csrf import csrf_exempt
import ast #para diccionario
import sqlite3
from django.contrib.auth.models import User
from .models import Player
from .models import Global
from .models import Plays
from django.contrib.auth.decorators import login_required   


def index(request):
    template = loader.get_template('boomSite/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('boomSite/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def stats(request):
    
    mydb = sqlite3.connect("db.sqlite3")
    curr = mydb.cursor()
    
    query_leaderboard ='''SELECT username, globalScore, level
        FROM boomSite_global
        ORDER BY globalScore DESC'''
    rows1 = curr.execute(query_leaderboard)
    data_leaderboard = []
    
    counter = 0
    for x in rows1:
        counter += 1
        data_leaderboard.append([counter, x[0], x[2], x[1]])
        
    
    query_timeFinish ='''SELECT username, timeFinish
        FROM boomSite_global
        WHERE level = 4
        ORDER BY timeFinish ASC
        LIMIT 3'''
    
    rows2 = curr.execute(query_timeFinish)
    data_timeFinish = []
    
    for x in rows2:
        data_timeFinish.append([x[0], x[1]])
        
    
    h_var = 'Country'
    v_var = 'Players'
    query_countries ='''SELECT country, COUNT(country)
		FROM boomSite_player
		GROUP BY country
	'''
    rows3 = curr.execute(query_countries)
    data = [[h_var, v_var]]
    
    for x in rows3:
        data.append([x[0], x[1]])

    modified_data = dumps(data)
    
    
 
 
    return render(request, 'boomSite/stats.html', {'values':data_leaderboard, 'values2': data_timeFinish, 'values3': modified_data})

def contact(request):
    template = loader.get_template('boomSite/contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        
        user = authenticate(request, username=username, password=pwd)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ('Bad login'))
            return render(request, 'boomSite/signin.html', {})
            
    else:
        return render(request, 'boomSite/signin.html', {})
        
    # template = loader.get_template('boomSite/signin.html')
    # context = {}
    # return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        #player_form = NewPlayerForm(request.POST, instance=request.user.player)
        if form.is_valid(): #and player_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.player.first_name = request.POST['first_name']
            user.player.username = request.POST['username']
            user.player.email = request.POST['email']
            user.player.password = request.POST['country']
            user.player.level = 1
            user.player.country = request.POST['country']
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ('Registration seccessful'))
            return redirect("index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            print(form.errors)
            return render(request, 'boomSite/signup.html', {'form': form})
    else:
        return render(request, 'boomSite/signup.html', {})

    # template = loader.get_template('boomSite/signup.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def profile(request):
    return render(request,'boomSite/profile.html')
    # template = loader.get_template('boomSite/profile.html')
    # context = {}
    # return HttpResponse(template.render(context, request))

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return render(request, 'boomSite/index.html', {})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        var = request.body
        dicc = ast.literal_eval(var.decode('utf-8'))
        # revisar que ['user'] existe
        u = Player.objects.filter(username=dicc['username'])
        return HttpResponse(str(json.dumps(u[0].toJson())).encode('utf-8'))
    else:
        return HttpResponse("Please use POST")


@csrf_exempt
def playing(request):
    if request.method == 'POST':
        var = request.body
        dicc1 = ast.literal_eval(var.decode('utf-8'))
        # revisar que ['user'] existe
        u = Global.objects.filter(username=dicc1['username'])
        print(u)
        if len (u) > 0:
            u3 = u[0]
            u3.globalScore=dicc1['globalScore']
            u3.timeFinish=dicc1['timeFinish']
            u3.timePlayed=dicc1['timePlayed']
            u3.level=dicc1['level']
            u3.save()
            return HttpResponse("ok".encode('utf-8'))
        else:
            p = request.body
            u2 = ast.literal_eval(p.decode('utf-8'))
            g = Global()
            g.username=u2['username']
            g.globalScore=u2['globalScore']
            g.timeFinish=u2['timeFinish']
            g.timePlayed=u2['timePlayed']
            g.level=u2['level']
            g.save()
            return HttpResponse("ok".encode('utf-8'))
    else:
        return HttpResponse("Please use POST")
        


@csrf_exempt
def level(request):
    if request.method == 'POST':
        p = request.body
        dicc3 = ast.literal_eval(p.decode('utf-8'))
        
        userSqlite = Player.objects.filter(username=dicc3['username'])
        u3 = userSqlite[0]
        u3.level=dicc3['level']
        u3.save()
        
        return HttpResponse("ok".encode('utf-8'))
    else:
        return HttpResponse("Please use POST")

@csrf_exempt
def plays(request):
    if request.method == 'POST':
        p = request.body
        u2 = ast.literal_eval(p.decode('utf-8'))
        pl = Plays()
        pl.username=u2['username']
        pl.score=u2['score']
        pl.attemps=u2['attemps']
        pl.timeToSolve=u2['timeToSolve']
        pl.level=u2['level']
        pl.save()
        return HttpResponse("ok".encode('utf-8'))
