# Generated by Django 4.1.1 on 2024-02-29 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainApp', '0002_snippet_is_hidden'),
    ]


    
    operations = [
    migrations.AddField(
        model_name='snippet',
        name='author',
        field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
    ),
]
