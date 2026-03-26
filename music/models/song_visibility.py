from django.db import models

class SongVisibility(models.TextChoices):
    PRIVATE = 'private', 'Private'
    PUBLIC = 'public', 'Public'