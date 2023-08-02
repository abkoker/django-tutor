from django.urls import path
from auth_app import views

app_name = 'auth_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('special/', views.special, name='special'),
    path('user_login/', views.user_login, name='user_login'),
]