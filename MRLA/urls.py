from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("foods/", include("foods.urls")),
    path("chat/", include("chat.urls")),
]
