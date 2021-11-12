from django.urls import path

from . import views


app_name = 'platform_working'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('users/', views.get_all_users, name='all_users'),
    path('albums/<int:album_id>/', views.get_album_with_album_list, name='album_list'),
    path('playlists/<int:playlist_id>/', views.get_playlist_with_playlist_list, name='playlist_list'),
]
