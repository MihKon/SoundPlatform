from django.http import HttpResponse
from django.shortcuts import render
from .models import Songs
from .models import Users
from .models import Albums
from .models import AlbumList
from .models import Groups
from .models import Playlists
from .models import PlaylistList
from .models import Reposts
from .models import Reviews
from .models import Subscriptions


# Create your views here.

def index(request):
    """
    будем использовать это, как приветственную страницу
    то есть - при попадании на эту страницу, пользователю будет предложено пройти авторизацию
    если же он уже авторизирован, будет осуществлен переход на глвную страницу
    """
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request, user_id):  # готово
    """
    в своём профиле авторизированный пользователь должен видеть все свои песни, подписки, альбомы, репосты
    """
    response = Songs.objects\
        .select_related('id_user').all()\
        .values('song_title', 'id_user__login', 'id_user__albums__album_title')\
        .filter(id_user=user_id)
    songs = get_songs_by_user_id(request, user_id)
    albums = get_album_by_user_id(request, user_id)
    playlists = Playlists.objects.all().filter(id_user__playlists=user_id)
    return render(request, 'platform_working/profile.html',
                  context={
                      "lst": response,
                      "songs": songs,
                      "albums": albums,
                      "playlists": playlists
                  })


def get_all_users(request):
    """
    вывод всех пользователей
    """
    response = Users.objects.all()
    context = {"lst": response}
    return render(request, 'platform_working/all_users.html', context)


def get_all_songs(request):
    """
    вывод всех песен
    """
    res = Songs.objects.all()
    return HttpResponse(res)


def get_all_albums(request):
    response = Albums.objects.all()
    return response


def get_all_playlists(request):
    res = Playlists.objects.all()
    return res


def get_all_groups(request):
    response = Groups.objects.all()
    return HttpResponse(response)


def get_user_by_login(request, login):
    """
    поиск пользователей по логину
    """
    res = Users.objects.filter(login=login).values('login', 'image')
    return HttpResponse(res)


def get_songs_by_title(request, title):
    res = Songs.objects.all().filter(song_title=title)
    return HttpResponse(res)


def get_albums_by_title(request, title):
    res = Albums.objects.all().filter(album_title=title)
    return res


def get_playlists_by_title(request, title):
    res = Playlists.objects.all().filter(playlist_title=title)
    return res


def get_groups_by_title(request, title):
    res = Groups.objects.all().filter(group_title=title)
    return res


def get_album_with_album_list(request, album_id):
    res = AlbumList.objects.all().filter(id_album=album_id)
    return HttpResponse(res)


def get_playlist_with_playlist_list(request, playlist_id):
    response = PlaylistList.objects.all().filter(id_playlist=playlist_id)
    return HttpResponse(response)


def get_songs_by_user_id(request, user_id):
    res = Songs.objects.all().filter(id_user=user_id)
    return res


def get_album_by_user_id(request, user_id):
    res = Albums.objects.all().filter(id_user=user_id)
    return res
