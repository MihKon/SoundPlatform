from django.urls import path

from . import views


app_name = 'platform_working'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.get_all_users, name='all_users'),
    path('search/', views.search, name='user_search'),
    path('users/profile/<int:user_id>/', views.profile, name='profile'),
    path('songs/', views.get_all_songs, name='all_songs'),
    path('songs/<int:song_id>/', views.get_song_by_id, name='song'),
    path('albums/', views.get_all_albums, name='all_albums'),
    path('albums/<int:album_id>/', views.get_album_with_album_list, name='album_list'),
    path('playlists/', views.get_all_playlists, name='all_playlists'),
    path('playlists/<int:playlist_id>/', views.get_playlist_with_playlist_list, name='playlist_list'),
    path('groups/', views.get_all_groups, name='all_groups'),
    path('groups/members/', views.get_users_by_group_id, name='group_members'),
]
