from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('schema/<int:pk>/', views.SchemaView.as_view(), name='schema'),
    path('schema/add/', views.SchemaCreateView.as_view(), name='create'),
    path('my/', views.DatasetView.as_view(), name='datasets'),
    path('download/<int:dataset_id>/', views.download, name='download'),
]
