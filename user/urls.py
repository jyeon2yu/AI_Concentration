from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.login),
    path('db_check/', views.db_check)
]