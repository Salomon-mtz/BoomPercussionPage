from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('stats/', views.stats, name='stats'),
    path('contact/', views.contact, name='contact'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name="logout_user"),
    path('login/', views.login_user, name="login_user"),
    path('playing/', views.playing, name="playing"),
    path('level/', views.level, name="level"),
     path('plays/', views.plays, name="plays"),
]