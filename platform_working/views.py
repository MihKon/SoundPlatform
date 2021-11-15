from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
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


#  готово (и метод, и шаблон)
def profile(request, user_id):
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


def search(request):
    query = request.GET.get('q')
    users = get_user_by_login(request, query)
    songs = get_songs_by_title(request, query)
    albums = get_albums_by_title(request, query)
    playlists = get_playlists_by_title(request, query)
    groups = get_groups_by_title(request, query)
    context = {
        "users": users,
        "songs": songs,
        "albums": albums,
        "playlists": playlists,
        "groups": groups
    }
    return render(request, 'platform_working/user_search.html', context)



def get_all_users(request):
    """
    вывод всех пользователей
    """
    response = Users.objects.all()
    context = {"lst": response}
    return render(request, 'platform_working/all_users.html', context)


def get_user_by_login(request, login):
    """
    поиск пользователей по логину
    """
    res = Users.objects.all().filter(
        Q(login__icontains=login)
    )
    return res


def create_user(request):
    email = request.POST['email']
    login = request.POST['login']
    password = request.POST['password']
    age = request.POST['age']
    image = request.POST['file']  # нужно будет исправить
    u = Users(email=email, login=login, password=password, age=age, image=image)
    u.save()


def get_all_songs(request):
    """
    вывод всех песен
    """
    res = Songs.objects.all()
    return HttpResponse(res)


def get_songs_by_title(request, title):
    res = Songs.objects.all().filter(
        Q(song_title__icontains=title)
    )
    return res


def get_songs_by_user_id(request, user_id):
    res = Songs.objects.all().filter(id_user=user_id)
    return res


def get_song_by_id(request, song_id):
    response = Songs.objects.all().filter(id_song=song_id)\
        .values('song_title', 'image', 'time', 'genre', 'id_user__albums__album_title',
                'id_user__playlists__playlist_title')
    rev = Reviews.objects.all().filter(id_song=song_id).values('id_reviewer__login', 'text', 'date')
    context = {'songs': response, "reviewers": rev}
    return render(request, 'platform_working/song.html', context)


def create_song(request):
    title = request.POST['title']
    file = request.POST['file']
    time = request.POST['time']
    user_id = request.user.id
    genre = request.POST['genre']
    image = request.POST['image']
    song = Songs(song_title=title, genre=genre, image=image, file=file, time=time, id_user=user_id)
    song.save()


def delete_song_by_id(request, song_id):
    song = Songs.objects.filter(id_song=song_id).delete()


def get_all_albums(request):
    response = Albums.objects.all()
    return HttpResponse(response)


def get_albums_by_title(request, title):
    res = Albums.objects.all().filter(
        Q(album_title__icontains=title)
    )
    return res


def get_album_with_album_list(request, album_id):
    res = AlbumList.objects.all().filter(id_album=album_id).values()
    return HttpResponse(res)


def get_album_by_user_id(request, user_id):
    res = Albums.objects.all().filter(id_user=user_id)
    return res


def get_all_playlists(request):
    res = Playlists.objects.all()
    return HttpResponse(res)


def get_playlists_by_title(request, title):
    res = Playlists.objects.all().filter(
        Q(playlist_title__icontains=title)
    )
    return res


def get_playlist_with_playlist_list(request, playlist_id):
    response = PlaylistList.objects.all().filter(id_playlist=playlist_id).values()
    return HttpResponse(response)


def get_all_groups(request):
    response = Groups.objects.all()
    return HttpResponse(response)


def get_groups_by_title(request, title):
    res = Groups.objects.all().filter(
        Q(group_title__icontains=title)
    )
    return res


def get_users_by_group_id(request, group_id):
    res = Subscriptions.objects.all().\
        values("id_follower__login", "id_follower_id", "id_follower__image").\
        filter(id_group=group_id)
    return res


def get_reviews_of_user(request):
    res = Reviews.objects.all().filter(id_reviewer=request.user.id)
    return res


def get_subscriptions_of_user(request):
    response = Subscriptions.objects.all().filter(id_follower=request.user.id)
    return response


def get_reposts_of_user(request):
    r = Reposts.objects.all().filter(id_reposter=request.user.id)
    return r
