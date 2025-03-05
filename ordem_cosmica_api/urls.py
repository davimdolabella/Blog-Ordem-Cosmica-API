from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = SimpleRouter()
app_name = 'ordem-cosmica-api'

router.register('article', views.ArticleViewSet, basename='article')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]