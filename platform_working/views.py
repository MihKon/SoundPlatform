from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
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
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request, user_id):
    response = Songs.objects\
        .select_related('id_user').all()\
        .values('song_title', 'id_user__login', 'id_user__albums__album_title', 'id_user__playlists__playlist_title')\
        .filter(id_user__songs=user_id)
    return HttpResponse(response)


def all_users(request):
    response = Users.objects.all()
    context = {"lst": response}
    return render(request, 'platform_working/all_users.html', context)


def get_all_songs(request):
    res = Songs.objects.all()
    return HttpResponse(res)


def get_user_by_name(request, login):
    res = Users.objects.filter(login=login).values('login', 'image')
    return HttpResponse(res)
