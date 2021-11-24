from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from .forms import *
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

id_const_user = 1


# Create your views here.

def index(request):
    """
    будем использовать это, как приветственную страницу
    то есть - при попадании на эту страницу, пользователю будет предложено пройти авторизацию
    если же он уже авторизирован, будет осуществлен переход на глвную страницу
    """
    return render(request, 'platform_working/index.html')


#  готово (и метод, и шаблон)
def profile(request, user_id):
    """
    в своём профиле авторизированный пользователь должен видеть все свои песни, подписки, альбомы, репосты
    """
    response = Songs.objects \
        .select_related('id_user').all() \
        .values('song_title', 'id_user__login', 'id_user__albums__album_title') \
        .filter(id_user=user_id)
    songs = get_songs_by_user_id(request, user_id)
    albums = get_album_by_user_id(request, user_id)
    playlists = Playlists.objects.all().filter(id_user__playlists=user_id)
    user = Users.objects.values('login', 'id_user').get(id_user=user_id)
    subs = Subscriptions.objects.filter(id_follower=user_id).values('id_user__groups__group_title', 'id_user__login',
                                                                    'id_user', 'id_group')
    revs = Reviews.objects.filter(id_user=user_id).all()
    lst = []
    for rev in revs:
        if rev.id_song is None:
            reviews = Reviews.objects.filter(id_review=rev.id_review).values('id_reviewer__login', 'text', 'date',
                                                                             'id_song', 'id_review',
                                                                             'id_reviewer').get()
            lst.append(reviews)
    reposts = Reposts.objects.filter(id_reposter=user_id).all().order_by('id_repost')
    reposted_songs = []
    for song in reposts:
        reposted_songs.append(Songs.objects.filter(id_song=song.id_song).values('id_song', 'id_user', 'id_user__login',
                                                                                'song_title').get())
    global id_const_user
    flag = True
    if user_id == id_const_user:
        flag = False
    subs_temp = Subscriptions.objects.filter(id_user=user_id)
    if subs_temp is not None:
        for i in subs_temp:
            if i.id_follower.id_user == id_const_user and i.id_group is None:
                flag = False
                break
    else:
        if user_id == id_const_user:
            flag = False

    if user_id == id_const_user:
        if not flag:
            context = {
                "lst": response,
                "songs": songs,
                "albums": albums,
                "playlists": playlists,
                "user": user,
                "subs": subs,
                "reviews": lst,
                "reposts": reposts,
                "reposted_songs": reposted_songs,
                "id_const": id_const_user
            }
        else:
            context = {"lst": response, "songs": songs, "albums": albums, "playlists": playlists,
                       "user": user, "subs": subs, "reviews": lst, "reposts": reposts, "reposted_songs": reposted_songs,
                       "id_const": id_const_user, "sub": 1}
    else:
        if flag:
            context = {"lst": response, "songs": songs, "albums": albums, "playlists": playlists,
                       "user": user, "subs": subs, "reviews": lst, "reposts": reposts, "reposted_songs": reposted_songs,
                       "sub": 1}
        else:
            context = {"lst": response, "songs": songs, "albums": albums, "playlists": playlists,
                       "user": user, "subs": subs, "reviews": lst, "reposts": reposts, "reposted_songs": reposted_songs}
    return render(request, 'platform_working/profile.html', context=context)


#  если оно будет работать всегда, то это успех
def hard_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            global id_const_user
            id_const_user = Users.objects.get(email=form.cleaned_data['email']).id_user
            return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
        else:
            print(form.cleaned_data)
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'platform_working/login.html', context=context)


#  готово (и метод, и шаблон)
def search(request):
    query = request.GET.get('q')
    users = get_user_by_login(request, query)
    songs = get_songs_by_title(request, query)
    albums = get_albums_by_title(request, query)
    playlists = get_playlists_by_title(request, query)
    groups = get_groups_by_title(request, query)
    global id_const_user
    context = {
        "users": users,
        "songs": songs,
        "albums": albums,
        "playlists": playlists,
        "groups": groups,
        "id_const": id_const_user
    }
    return render(request, 'platform_working/user_search.html', context)


#  готово (и метод, и шаблон)
def get_all_users(request):
    """
    вывод всех пользователей
    """
    response = Users.objects.all()
    global id_const_user
    context = {"lst": response, "id_const": id_const_user}
    return render(request, 'platform_working/all_users.html', context)


#  используется
def get_user_by_login(request, login):
    """
    поиск пользователей по логину
    """
    res = Users.objects.all().filter(
        Q(login__icontains=login)
    )
    return res


# готово (и метод, и шаблон)
def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            u = Users.objects.get(login=form.cleaned_data['login'])
            global id_const_user
            id_const_user = u.id_user
            return HttpResponseRedirect(reverse('platform_working:profile', args=(u.id_user,)))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'platform_working/new_user.html', context=context)


#  живём
def update_user(request):
    global id_const_user
    user = Users.objects.get(id_user=id_const_user)
    form = UpdateUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
    return render(request, 'platform_working/update_user.html', context={'form': form})


def delete_user(request):
    global id_const_user
    Users.objects.get(id_user=id_const_user).delete()
    return render(request, 'platform_working/index.html')


#  готово (и метод, и шаблон)
def get_all_songs(request):
    """
    вывод всех песен
    """
    res = Songs.objects.all()
    global id_const_user
    return render(request, 'platform_working/all_songs.html', context={"lst": res, "id_const": id_const_user})


#  используется
def get_songs_by_title(request, title):
    res = Songs.objects.all().filter(
        Q(song_title__icontains=title)
    )
    return res


#  используется
def get_songs_by_user_id(request, user_id):
    res = Songs.objects.all().filter(id_user=user_id)
    return res


#  готово (и метод, и шаблон)
def get_song_by_id(request, song_id):
    response = Songs.objects.filter(id_song=song_id).get()
    rev = Reviews.objects.all().filter(id_song=song_id).values('id_reviewer__login', 'text', 'date', 'id_reviewer')
    title = Songs.objects.get(id_song=song_id)
    user = Users.objects.filter(id_user=title.id_user.id_user).get()
    albums = AlbumList.objects.filter(id_song=song_id).values('id_album__album_title', 'id_album')
    mixes = PlaylistList.objects.filter(id_song=song_id).values('id_playlist__playlist_title', 'id_playlist')
    time = response.time.strftime("%H:%M:%S")
    global id_const_user
    if user.id_user == id_const_user:
        context = {'song': response, 'reviews': rev, 'title': title, 'albums': albums,
                   'playlists': mixes, 'author': user, 'time': time, 'id_const': id_const_user}
    else:
        context = {'song': response, 'reviews': rev, 'title': title, 'albums': albums,
                   'playlists': mixes, 'author': user, 'time': time}
    return render(request, 'platform_working/song.html', context)


#  живём
def create_song(request):
    if request.method == 'POST':
        global id_const_user
        form = AddSongForm(request.POST)
        if form.is_valid():
            minutes = form.cleaned_data['time'].hour
            sec = form.cleaned_data['time'].minute
            time = form.cleaned_data['time'].replace(hour=0, minute=minutes, second=sec)
            form.cleaned_data['time'] = time
            form.cleaned_data['id_user'] = Users.objects.get(id_user=id_const_user)
            Songs.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
    else:
        form = AddSongForm()
    return render(request, 'platform_working/new_song.html', context={'form': form})


#  живём
def update_song(request, song_id):
    song = Songs.objects.get(id_song=song_id)
    form = UpdateSongForm(request.POST or None, instance=song)
    if form.is_valid():
        try:
            form.save()
            return HttpResponseRedirect(reverse('platform_working:song', args=(song.id_song,)))
        except:
            form.add_error(None, 'Ошбика обновления песни')

    return render(request, 'platform_working/update_song.html', context={'form': form})


#  готово, но стоит поработать над тем, чтобы удалять песни и из других таблиц (или написать триггер)
def delete_song_by_id(request, song_id):
    user_id = Songs.objects.get(id_song=song_id).id_user
    Songs.objects.get(id_song=song_id).delete()
    return HttpResponseRedirect(reverse('platform_working:profile', args=(user_id.id_user,)))


#  готово (и метод, и шаблон)
def get_all_albums(request):
    response = Albums.objects.all()
    global id_const_user
    return render(request, 'platform_working/all_albums.html', context={"lst": response, "id_const": id_const_user})


#  используется
def get_albums_by_title(request, title):
    res = Albums.objects.all().filter(
        Q(album_title__icontains=title)
    )
    return res


#  готово (и метод, и шаблон)
def get_album_with_album_list(request, album_id):
    res = AlbumList.objects.all().filter(id_album=album_id).order_by('number')
    title = Albums.objects.get(id_album=album_id).album_title
    author = Users.objects.get(id_user=Albums.objects.get(id_album=album_id).id_user.id_user)
    global id_const_user
    if author.id_user == id_const_user:
        context = {"album": res, "title": title, "author": author, "id_const": id_const_user}
    else:
        context = {"album": res, "title": title, "author": author}
    return render(request, 'platform_working/albums_lists.html', context=context)


#  используется
def get_album_by_user_id(request, user_id):
    res = Albums.objects.all().filter(id_user=user_id)
    return res


def create_album(request):
    if request.method == 'POST':
        global id_const_user
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            form.cleaned_data['id_user'] = Users.objects.get(id_user=id_const_user)
            album = Albums(**form.cleaned_data)
            print(album.objects)
            #  return HttpResponseRedirect(reverse('platform_working:create_album_list', args=(album.id_album,)))
    else:
        form = AddAlbumForm()
    return render(request, 'platform_working/new_album.html', context={'form': form})


def create_album_list(request, album_id):
    if request.method == 'POST':
        form = 0
    return 0


def update_album(request, album_id):
    return 1


def update_album_list(request, album_id, song_id):
    return 1


def delete_album_by_id(request, album_id):
    Albums.objects.filter(id_album=album_id).delete()
    return render(request, 'platform_working/all_albums.html')


#  готово (и метод, и шаблон)
def get_all_playlists(request):
    res = Playlists.objects.all()
    global id_const_user
    context = {"lst": res, "id_const": id_const_user}
    return render(request, 'platform_working/all_playlists.html', context=context)


#  используется
def get_playlists_by_title(request, title):
    res = Playlists.objects.all().filter(
        Q(playlist_title__icontains=title)
    )
    return res


#  готово (и метод, и шаблон)
def get_playlist_with_playlist_list(request, playlist_id):
    response = PlaylistList.objects.all().filter(id_playlist=playlist_id).order_by('number')
    title = Playlists.objects.get(id_playlist=playlist_id).playlist_title
    author = Users.objects.get(id_user=Playlists.objects.get(id_playlist=playlist_id).id_user.id_user)
    lst = []
    pl = PlaylistList.objects.filter(id_playlist=playlist_id).all()
    for r in pl:
        user_id = Songs.objects.get(id_song=r.id_song).id_user.id_user
        user = Users.objects.get(id_user=user_id)
        if lst.count(user) == 0:
            lst.append(user)
    global id_const_user
    if author.id_user == id_const_user:
        context = {"title": title, "author": author, "playlist": response, "users": lst, "id_const": id_const_user}
    else:
        context = {"title": title, "author": author, "playlist": response, "users": lst}
    return render(request, 'platform_working/playlists_lists.html', context=context)


def create_playlist(request):
    title = request.POST['title']
    time = request.POST['time']
    user = request.user.id
    mix = Playlists(playlist_title=title, time=time, id_user=user)
    mix.save()


def create_playlist_list(request, playlist_id):
    return 0


def update_playlist(request, playlist_id):
    return 1


def update_playlist_list(request, playlist_id, song_id):
    return 1


def delete_playlist_by_id(request, mix_id):
    Playlists.objects.filter(id_playlist=mix_id).delete()


#  готово (и метод, и шаблон)
def get_all_groups(request):
    res = Groups.objects.all()
    global id_const_user
    return render(request, 'platform_working/all_groups.html', context={"lst": res, "id_const": id_const_user})


#  используется
def get_groups_by_title(request, title):
    res = Groups.objects.all().filter(
        Q(group_title__icontains=title)
    )
    return res


def create_group(request):
    creator = Users.objects.filter(id_user=request.user.id).values('login')
    title = request.POST['title']
    des = request.POST['description']
    user = request.user.id
    group = Groups(creator=creator, group_title=title, description=des, id_user=user)
    group.save()


def update_group(request, group_id):
    return 1


def delete_group_by_id(request, group_id):
    Groups.objects.filter(id_group=group_id).delete()


#  готово (и метод, и шаблон)
def get_users_by_group_id(request, group_id):
    res = Subscriptions.objects.all(). \
        values("id_follower__login", "id_follower_id", "id_follower__image", "id_group", "id_follower",
               "id_user__groups__group_title", "id_user__login", "id_user"). \
        filter(id_group=group_id)
    user_id = Groups.objects.get(id_group=group_id).id_user.id_user
    user = Users.objects.get(id_user=user_id)
    title = Groups.objects.get(id_group=group_id).group_title
    global id_const_user
    flag = False
    for i in Subscriptions.objects.filter(id_group=group_id):
        if i.id_follower == id_const_user:
            flag = True
            break
    if not flag:
        context = {"group": res, "title": title, "user": user, "id_g": group_id, "id_const": id_const_user}
    else:
        context = {"group": res, "title": title, "user": user}
    return render(request, 'platform_working/group_members.html', context=context)


# def get_reviews_of_user(request, user_id):
#     res = Reviews.objects.all().filter(id_reviewer=user_id)
#     return res


def create_review(request):
    text = request.POST['text']
    date = request.POST['date']
    reviewer = request.user.id
    song = request.POST['song']
    user = request.POST['user']
    rev = Reviews(text=text, date=date, id_reviewer=reviewer, id_song=song, id_user=user)
    rev.save()


def delete_review(request, review_id):
    Reviews.objects.filter(id_review=review_id).delete()


# def get_subscriptions_of_user(request, user_id):
#     response = Subscriptions.objects.all().filter(id_follower=user_id)
#     return response


def create_sub(request):
    follower = request.user.id
    group = request.POST['group']
    user = request.POST['user']
    sub = Subscriptions(id_follower=follower, id_group=group, id_user=user)
    sub.save()


def delete_sub(request, sub_id):
    Subscriptions.objects.filter(id_subscription=sub_id).delete()


# def get_reposts_of_user(request, user_id):
#     r = Reposts.objects.all().filter(id_reposter=user_id)
#     return r


def create_repost(request):
    text = request.POST['text']
    song = request.POST['song']
    reposter = request.user.id
    user = request.POST['user']
    repost = Reposts(text=text, id_song=song, id_reposter=reposter, id_user=user)
    repost.save()


def delete_repost(request, rep_id):
    Reposts.objects.filter(id_repost=rep_id).delete()
