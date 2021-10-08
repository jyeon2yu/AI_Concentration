from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # path('', views.webcam, name='webcam'),
    path('report/', views.report_chart, name='report'),
    path('subject_data/', views.subject_data),
    path('subject_data_week/', views.subject_data_week),
    path('conc_daily/', views.conc_daily, name='conc_daily'),
    path('conc_week/', views.conc_week, name='conc_week'),
    path('emotion_daily/', views.emotion_daily, name='emotion_daily'),
    path('emotion_week/', views.emotion_week, name='emotion_week'),

]