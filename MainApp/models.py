from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=True)
