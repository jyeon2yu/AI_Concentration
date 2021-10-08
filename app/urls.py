from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # path('', views.webcam, name='webcam'),
    path('report/', views.report_chart, name='report'),
    path('data/', views.report_data, name='data'),
    path('subject_data/', views.subject_data),
    path('subject_data_week/', views.subject_data_week),
]