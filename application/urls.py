from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('music/genre/', views.GenreView, name='genre'),
    path('music/genre/<str:gen>/', views.genre_detail, name='genre_detail'),
    path('music/artist/<str:author>/', views.artist_detail, name='artist_detail'),
    path('music/track/<str:name>/', views.SingleTrackDetail, name='single_track_detail'),
    path('music/album/<str:pk>/', views.album_detail, name='album_detail'),
    path('music/artist/<str:gen>/all_tracks', views.all_tracks, name='all_tracks'),
    path('contact/', views.contact_page, name='contact_page')
]