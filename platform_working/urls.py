from django.urls import path

from . import views


app_name = 'platform_working'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('users/', views.all_users, name='all_users')
]
