from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('prediction/', views.prediction, name='prediction'),
    path('query/', views.query, name='query'),
]
