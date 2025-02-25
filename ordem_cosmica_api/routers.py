from rest_framework.routers import SimpleRouter
from . import views

ArticleRouter = SimpleRouter()
ArticleRouter.register(
    'article',
    viewset=views.ArticleViewSet,
    basename='ordem-cosmica-api-article'
)

CommentRouter = SimpleRouter()
CommentRouter.register(
    'comment',
    viewset=views.CommentViewSet,
    basename='ordem-cosmica-api-comment'
)


ProfileRouter = SimpleRouter()
ProfileRouter.register(
    'profile',
    viewset=views.ProfileViewSet,
    basename='ordem-cosmica-api-profile'
)