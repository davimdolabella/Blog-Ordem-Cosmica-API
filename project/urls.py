
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ordem-cosmica-api/', include('ordem_cosmica_api.urls')),
]
