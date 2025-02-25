from django.urls import path, include
from . import views, routers



urlpatterns = [
    path('',include(routers.ArticleRouter.urls)),
    path('',include(routers.CommentRouter.urls)),
    path('',include(routers.ProfileRouter.urls)),
]
