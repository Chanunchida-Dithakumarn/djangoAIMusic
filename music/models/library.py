from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    user = models.ForeignKey('music.User', on_delete=models.CASCADE, related_name='libraries')

    def __str__(self):
        return self.name