from django.db import models
from django.conf import settings
# Create your models here.



class TodoItem(models.Model):
  
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.IntegerField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.title
