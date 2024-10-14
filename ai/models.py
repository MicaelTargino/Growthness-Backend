from django.db import models

# Create your models here.
class AI_data(models.Model):
    goal = models.CharField(max_length=255)
    json_data = models.JSONField()