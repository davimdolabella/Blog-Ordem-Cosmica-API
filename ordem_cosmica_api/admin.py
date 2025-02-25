from django.contrib import admin
from . import models

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...