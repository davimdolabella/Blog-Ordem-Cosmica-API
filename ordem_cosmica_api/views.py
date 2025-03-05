from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers, models
from . import permissions

class OrdemCosmicaAPIPagination(PageNumberPagination):
    page_size = 1

class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all().order_by('-created_at')
    serializer_class = serializers.ArticleSerializer
    http_method_names= ['get', 'patch', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = OrdemCosmicaAPIPagination
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()

class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all().order_by('-id')
    serializer_class = serializers.CommentSerializer
    http_method_names= ['get', 'patch', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = OrdemCosmicaAPIPagination
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()

class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all().order_by('-id')
    serializer_class = serializers.ProfileSerializer
    http_method_names= ['get', 'patch', 'post','delete']
    pagination_class = OrdemCosmicaAPIPagination
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsOwner(),]
        return super().get_permissions()




