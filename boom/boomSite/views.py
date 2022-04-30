import chunk
from fileinput import filename
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm
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
import hashlib
import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os


def index(request):
    template = loader.get_template('boomSite/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

# def download(request):
    

def about(request):
    template = loader.get_template('boomSite/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def stats(request):
    
    #Conexión con la base de datos
    mydb = sqlite3.connect("db.sqlite3")
    curr = mydb.cursor()
    
    #Leaderboard query
    query_leaderboard ='''SELECT username, globalScore, level
        FROM boomSite_global
        ORDER BY globalScore DESC'''
    rows1 = curr.execute(query_leaderboard)
    data_leaderboard = []
    
    counter = 0
    for x in rows1:
        counter += 1
        data_leaderboard.append([counter, x[0], x[2], x[1]])
        
    
    #Time Finish Query
    query_timeFinish ='''SELECT username, timeFinish
        FROM boomSite_global
        WHERE level = 4
        ORDER BY timeFinish ASC
        LIMIT 3'''
    
    rows2 = curr.execute(query_timeFinish)
    data_timeFinish = []
    
    for x in rows2:
        data_timeFinish.append([x[0], x[1]])
        
    
    #Map Query
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
    
    #Sin Stats Query
    curr.execute("SELECT * FROM boomSite_global")
    res = curr.fetchall()
    empty = len(res)

    #Time Played Query
    ht1 = 'Username'
    ht2 = 'Time Played'
    tiemposJugados = curr.execute("SELECT username, timePlayed FROM boomSite_global ORDER BY timePlayed DESC")
    successtj = [[ht1 , ht2]]
    
    for x in tiemposJugados:
        successtj.append([x[0], x[1]])
    tiemposJugados = dumps(successtj)
    
    #Sin level graph Query
    curr.execute("SELECT * FROM boomSite_global WHERE level = 4")
    res = curr.fetchall()
    level = len(res)
    
    #Levels per Username Query
    hl1 = 'Username'
    hl2 = 'Level'
    nivelesJugadores = curr.execute("SELECT username, level FROM boomSite_global ORDER BY level ASC")
    successlj = [[hl1 , hl2]]
    
    for y in nivelesJugadores:
        successlj.append([y[0], y[1]])
    nivelesJugadores = dumps(successlj)
    
    #Player Counter Query
    
    h_var = 'Number'
    v_var = 'Players'
    qPlayers = curr.execute("SELECT COUNT (DISTINCT user_id) FROM boomSite_player")
    data = []
    
    for x in qPlayers:
        data.append(x[0])
        t = data[0]
        print(t)

    total_players = dumps(data)

    curr.execute("SELECT * FROM boomSite_global")
    res = curr.fetchall()
    empty = len(res)

    return render(request, 'boomSite/stats.html', {'values':data_leaderboard, 'values2': data_timeFinish, 'valoresTiempo': tiemposJugados,'values3': modified_data, 'emptyStats': empty, 'emptyLevel': level, 'niveles':nivelesJugadores, 'number': t})

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


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            user.refresh_from_db()
            user.player.first_name = request.POST['first_name']
            user.player.username = request.POST['username']
            user.player.email = request.POST['email']
            pwd = hashlib.md5(request.POST['password1'].encode())
            user.player.password = pwd.hexdigest().upper()
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


@login_required
def profile(request):
    mydb = sqlite3.connect("db.sqlite3")
    curr = mydb.cursor()

    #GLOBAL SCORE USER
    userStr = request.user.username
    val = (userStr, )
    curr.execute("SELECT globalScore FROM boomSite_global WHERE username = ? ", val)
    res = curr.fetchall()
    
    for row in res:
        gS = row[0]
    
    #LEVELS ACCOMPLISH USER
    curr.execute("SELECT level FROM boomSite_player WHERE username = ? ", val)
    res2 = curr.fetchall()
    
    for row in res2:
        aL = row[0]
        
    #HISTORIC SCORES USER
    rows1 = curr.execute("SELECT score, level FROM boomSite_plays WHERE username = ? ", val)
    personalScores = []

    for x in rows1:
        personalScores.append([x[0], x[1]])
        
    
    #ATTEMPTS VS LEVELS PLAYED
    h = 'Level'
    v = 'Attempts'
    s = curr.execute("SELECT attempts, level FROM boomSite_plays WHERE username = ? ", val)
    success = [[h , v]]
    
    for x in s:
        success.append([x[1], x[0]])
    s = dumps(success)
    
    
    #PLAYER GLOBAL RANKING POSITION
    leaderboard =curr.execute("SELECT username, globalScore, level FROM boomSite_global ORDER BY globalScore DESC")
    data_leaderboard = []
    counter = 0
    for x in leaderboard:
        counter += 1
        data_leaderboard.append([counter, x[0], x[2], x[1]])
    position = -1
    for y in data_leaderboard:
        if y[1] == userStr:
            position = y[0]
            print(position)
            break
    
    
    #NOMBRE
    curr.execute("SELECT username FROM auth_user WHERE username = ?", val)
    n = curr.fetchall()
    
    for x in n:
        nombre = x[0]
        
        
    #LAST LOGIN
    curr.execute("SELECT last_login FROM auth_user WHERE username = ?", val)
    last = curr.fetchall()
    
    for x in last:
        lastLog = x[0]
        
    
    return render(request,'boomSite/profile.html', {'userGlobalScore': gS, 'levelAccomplish': aL, 'scores': personalScores, 'success':s, 'rank': position, 'name': nombre, 'last':lastLog })


def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return render(request, 'boomSite/index.html', {})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        var = request.body
        dicc = ast.literal_eval(var.decode('utf-8'))
        u = Player.objects.filter(username=dicc['username'])
        return HttpResponse(str(json.dumps(u[0].toJson())).encode('utf-8'))
    else:
        return HttpResponse("Please use POST")


@csrf_exempt
def playing(request):
    if request.method == 'POST':
        var = request.body
        dicc1 = ast.literal_eval(var.decode('utf-8'))
        u = Global.objects.filter(username=dicc1['username'])
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
        var = request.body
        dicc4 = ast.literal_eval(var.decode('utf-8'))
        p = Plays.objects.filter(username=dicc4['username'])
        if len(p) == 0:
            p = request.body
            u2 = ast.literal_eval(p.decode('utf-8'))
            pl = Plays()
            pl.username=u2['username']
            pl.score=u2['score']
            pl.attempts=u2['attempts']
            pl.timeToSolve=u2['timeToSolve']
            pl.level=u2['level']
            pl.save() 
        u = Plays.objects.filter(level=dicc4['level'], username=dicc4['username'])
        if len (u) > 0:
            u3 = u[0]
            u3.score=dicc4['score']
            u3.attempts=dicc4['attempts']
            u3.timeToSolve=dicc4['timeToSolve']
            u3.save()
            print("Atualizar", u3)
            return HttpResponse("ok".encode('utf-8'))
        else:
            p = request.body
            u2 = ast.literal_eval(p.decode('utf-8'))
            pl = Plays()
            pl.username=u2['username']
            pl.score=u2['score']
            pl.attempts=u2['attempts']
            pl.timeToSolve=u2['timeToSolve']
            pl.level=u2['level']
            pl.save()
            print("Crear", pl)
            return HttpResponse("ok".encode('utf-8'))
    else:
        return HttpResponse("Please use POST")