from django.urls import path
from . import views

app_name = 'autors_app'

urlpatterns = [
    path('', views.main, name='index'),
]