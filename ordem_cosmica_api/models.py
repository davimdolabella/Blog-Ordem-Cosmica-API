from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='profiles/images/%Y/%m/%d/', blank=True, default='')  # Pode ser vazio, mas não obrigatório

    def __str__(self):
        return self.user.username
    

class Article(models.Model):
    title = models.CharField(max_length=60, blank=False, null=False)  
    description = models.CharField(max_length=150, blank=False, null=False)  
    content = models.TextField(blank=False, null=False)  
    image = models.ImageField(upload_to='articles/images/%Y/%m/%d/', blank=True, default='')  # Opcional
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=False
    )  

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments'
    )  
    content = models.CharField(max_length=150, blank=False, null=False)  
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments'
    )  

    def __str__(self):
        return f'{self.author} to {self.article}'
