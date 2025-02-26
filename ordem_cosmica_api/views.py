from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers, models
from . import permissions

class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    http_method_names= ['get', 'patch', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()

class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    http_method_names= ['get', 'patch', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly,]
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()

class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    http_method_names= ['get', 'patch', 'post','delete']
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()




