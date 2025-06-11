from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Servir arquivos de mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
