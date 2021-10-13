from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    # path('login/', views.login),
    path('profile/', views.profile, name="profile"),
    path('mypage/', views.mypage, name='mypage'),

    path('logout/', views.logout, name="logout"),

    path('', views.login, name="login"),
    path('check_user', views.check_user, name="check_user")

    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    # path('main/', views.main, name='main'),
    # path('profile/', views.profile, name='profile')
]