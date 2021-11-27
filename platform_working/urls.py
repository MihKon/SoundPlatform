from django.urls import path

from . import views


app_name = 'platform_working'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.get_all_users, name='all_users'),  # готово
    path('search/', views.search, name='user_search'),  # готово
    path('users/login/', views.hard_login, name='hard_login'),
    path('users/profile/<int:user_id>/', views.profile, name='profile'),  # готово
    path('users/profile/update', views.update_user, name='update_user'),
    path('users/profile/<int:user_id>/delete', views.delete_user, name='delete_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('songs/', views.get_all_songs, name='all_songs'),  # готово
    path('songs/<int:song_id>/', views.get_song_by_id, name='song'),  # готово
    path('songs/<int:song_id>/update', views.update_song, name='update_song'),
    path('songs/<int:song_id>/delete', views.delete_song_by_id, name='delete_song'),
    path('songs/create/', views.create_song, name='create_song'),
    path('albums/', views.get_all_albums, name='all_albums'),  # готово
    path('albums/<int:album_id>/', views.get_album_with_album_list, name='album_list'),  # готово
    path('albums/<int:album_id>/update', views.update_album, name='update_album'),
    path('albums/<int:album_id>/delete', views.delete_album_by_id, name='delete_album'),
    path('albums/create', views.create_album, name='create_album'),
    path('albums/<int:album_id>/create', views.create_album_list, name='create_album_list'),
    path('playlists/', views.get_all_playlists, name='all_playlists'),  # готово
    path('playlists/create', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.get_playlist_with_playlist_list, name='playlist_list'),  # готово
    path('playlists/<int:playlist_id>/update', views.update_playlist, name='update_playlist'),
    path('playlists/<int:playlist_id>/delete', views.delete_playlist_by_id, name='delete_playlist'),
    path('playlists/<int:playlist_id>/create', views.create_playlist_list, name='create_playlist_list'),
    path('groups/', views.get_all_groups, name='all_groups'),  # готово
    path('groups/<int:group_id>/update', views.update_group, name='update_group'),
    path('groups/<int:group_id>/delete', views.delete_group_by_id, name='delete_group'),
    path('groups/<int:group_id>/members/', views.get_users_by_group_id, name='group_members'),  # готово
    path('groups/create', views.create_group, name='create_group'),
    path('users/profile/<int:user_id>/review/create', views.create_review_on_user, name='create_review_on_user'),
    path('users/profile/<int:user_id>/review_create/delete', views.delete_review_on_user, name='delete_review_on_user'),
    path('songs/<int:song_id>/review/create', views.create_review_on_song, name='create_review_on_song'),
    path('songs/<int:song_id>/review_create/delete', views.delete_review_on_song, name='delete_review_on_song'),
    path('users/profile/<int:user_id>/sub', views.create_sub, name='create_sub_on_user'),
    path('users/profile/<int:user_id>/sub/delete', views.delete_sub_on_user, name='delete_sub_on_user'),
    path('groups/<int:group_id>/members/sub', views.create_sub, name='create_sub_on_group'),
    path('groups/<int:group_id>/members/sub/delete', views.delete_sub_on_group, name='delete_sub_on_group'),
    path('songs/<int:song_id>/repost', views.create_repost, name='create_repost'),
    path('songs/<int:song_id>/repost/delete', views.delete_repost, name='delete_repost'),
]
