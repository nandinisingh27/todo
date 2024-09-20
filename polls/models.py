from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.




class TodosItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255,default=None)
    username = models.CharField(max_length=255,default=None)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    id = models.IntegerField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.title
