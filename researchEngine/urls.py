from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('upload/', views.upload_document, name='upload_document'),
    path('prediction/', views.prediction, name='prediction'),
    path('query/', views.query_view, name='query'),
]
