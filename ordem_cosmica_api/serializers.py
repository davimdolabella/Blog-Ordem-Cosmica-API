from rest_framework import serializers
from . import models

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = models.Profile
        fields = ['id', 'user', 'username','email', 'password', 'image']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        }
        user = models.User.objects.create_user(**user_data)  
        profile = models.Profile.objects.create(user=user, **validated_data) 
        return profile

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'content', 'article']

class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = models.Article
        fields = ['id','author', 'title', 'description', 'content', 'image', 'created_at', 'comments']