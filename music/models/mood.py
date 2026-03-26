from django.db import models

class Mood(models.TextChoices):
    HAPPY = 'happy', 'Happy'
    SAD = 'sad', 'Sad'
    ROMANTIC = 'romantic', 'Romantic'
    RELAXED = 'relaxed', 'Relaxed'
    ENERGETIC = 'energetic', 'Energetic'
    CALM = 'calm', 'Calm'
    ANGRY = 'angry', 'Angry'