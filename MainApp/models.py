from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .validators import validate_image_extension, validate_image_size

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=True)

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='comments', verbose_name='Сниппет')
    image = models.ImageField(upload_to='comments_images/', null=True, blank=True, validators=[validate_image_extension, validate_image_size])

    def __str__(self):
        return f'Комментарий от {self.author} к {self.snippet}'
