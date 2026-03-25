from django.db import models


class Mood(models.TextChoices):
    HAPPY = 'happy', 'Happy'
    SAD = 'sad', 'Sad'
    ROMANTIC = 'romantic', 'Romantic'
    RELAXED = 'relaxed', 'Relaxed'
    ENERGETIC = 'energetic', 'Energetic'
    CALM = 'calm', 'Calm'
    ANGRY = 'angry', 'Angry'


class Genre(models.TextChoices):
    POP = 'pop', 'Pop'
    ROCK = 'rock', 'Rock'
    JAZZ = 'jazz', 'Jazz'
    CLASSICAL = 'classical', 'Classical'
    HIPHOP = 'hiphop', 'Hip Hop'
    RNB = 'rnb', 'R&B'


class SongVisibility(models.TextChoices):
    PRIVATE = 'private', 'Private'
    PUBLIC = 'public', 'Public'


class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Library(models.Model):
    name = models.CharField(max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libraries')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    mood = models.CharField(max_length=50, choices=Mood.choices)
    genre = models.CharField(max_length=50, choices=Genre.choices)
    visibility = models.CharField(max_length=20, choices=SongVisibility.choices, default=SongVisibility.PRIVATE)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    cover_image = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')

    def __str__(self):
        return self.title
