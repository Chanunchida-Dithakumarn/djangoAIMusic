from django.db import models

from .mood import Mood
from .genre import Genre
from .song_visibility import SongVisibility
from .status import Status

class Song(models.Model):
    title = models.CharField(max_length=200)
    mood = models.CharField(max_length=50, choices=Mood.choices)
    genre = models.CharField(max_length=50, choices=Genre.choices)
    visibility = models.CharField(max_length=20, choices=SongVisibility.choices, default=SongVisibility.PRIVATE)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    cover_image = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # -------- for API --------
    task_id = models.CharField(max_length=255, blank=True, null=True)
    song_url = models.URLField(blank=True, null=True)

    user = models.ForeignKey('music.User', on_delete=models.CASCADE, related_name='songs')
    library = models.ForeignKey('music.Library', on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')

    def __str__(self):
        return self.title