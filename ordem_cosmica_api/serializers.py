from rest_framework import serializers
from . import models
import re
from rest_framework.serializers import ValidationError

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
    def validate_password(self, value):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

        if not regex.match(value):
            raise ValidationError((
                'Password must have at least one uppercase letter, '
                'one lowercase letter and one number. The length should be '
                'at least 8 characters.'
            ),
                code='invalid'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    def create(self, validated_data):
        author = models.Profile.objects.filter(user = self.context.get('request').user).first() 
        comment = models.Comment.objects.create(author=author, **validated_data)
        return comment
    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'content', 'article']

class ArticleSerializer(serializers.ModelSerializer):
    author= ProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    def create(self, validated_data):
        author = models.Profile.objects.filter(user = self.context.get('request').user).first() 
        article = models.Article.objects.create(author=author, **validated_data)
        return article
    class Meta:
        model = models.Article
        fields = ['id','author', 'title', 'description', 'content', 'image', 'created_at', 'comments']