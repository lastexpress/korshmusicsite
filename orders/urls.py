from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from application import views

app_name = 'application'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('application.urls', namespace='application')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)