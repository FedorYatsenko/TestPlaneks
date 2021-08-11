from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datasets/', include('datasets.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
