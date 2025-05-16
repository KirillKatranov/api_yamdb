from django.db import models
from django.utils import timezone
import datetime

from users.models import CustomUser

class EmailVerificationCode(models.Model):
    email = models.EmailField()
    confirmation_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)
    
class Genre(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)

class Title(models.Model):
    name = models.CharField(max_length=60)
    year = models.IntegerField()
    description = models.TextField(max_length=2000)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, related_name='category', 
        on_delete=models.SET_NULL,
        null=True
        )

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)



class Reviews(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    title = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews")

class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")
    reviews = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()



