from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

from .forms import CustomAuthForm

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datasets/', include('datasets.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
