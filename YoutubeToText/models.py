from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Worldcities(models.Model):
    city = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)  # This field type is a guess.
    lng = models.TextField(blank=True, null=True)  # This field type is a guess.
    country = models.TextField(blank=True, null=True)
    id = models.TextField(blank=True, primary_key=True)  #UN MODEL TRB SA AIBA UN PRIMARY KEY

    class Meta:
        managed = False
        db_table = 'worldcities'

class ConvertedVideo(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  # Cele mai recente primele

    def __str__(self):
        return self.title
