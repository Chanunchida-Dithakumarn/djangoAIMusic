from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.generate_song, name='generate_song'),
    path('detail/<int:song_id>/', views.song_detail, name='song_detail'),
]