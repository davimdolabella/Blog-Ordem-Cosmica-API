from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='profiles/images/%Y/%m/%d/', default='')
    def __str__(self):
        return self.user.username
    

class Article(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/images/%Y/%m/%d/', default='')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True
    )
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments'
    )
    content = models.CharField(max_length=150)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments'
    )
    def __str__(self):
        return f'{self.author} to {self.article}'
    
