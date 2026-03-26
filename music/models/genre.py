from django.db import models

class Genre(models.TextChoices):
    POP = 'pop', 'Pop'
    ROCK = 'rock', 'Rock'
    JAZZ = 'jazz', 'Jazz'
    CLASSICAL = 'classical', 'Classical'
    HIPHOP = 'hiphop', 'Hip Hop'
    RNB = 'rnb', 'R&B'