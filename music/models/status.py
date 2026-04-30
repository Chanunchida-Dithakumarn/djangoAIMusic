from django.db import models

class Status(models.TextChoices):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    COMPLETED = 'Completed'