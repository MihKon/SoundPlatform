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
from datetime import datetime

id_const_user = 1


# Create your views here.
# есть
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
                       "user": user, "subs": subs, "reviews": lst, "reposts": reposts, "reposted_songs": reposted_songs,
                       "del_sub": 1}
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


#  готово (но может и нет, надо пробовать)
def delete_user(request):
    global id_const_user
    users_to_delete = Subscriptions.objects.filter(id_user=id_const_user)
    for user in users_to_delete:
        user.delete()
    users_to_delete = Groups.objects.filter(id_user=id_const_user)
    for user in users_to_delete:
        user.delete()
    users_to_delete = Reposts.objects.filter(id_user=id_const_user)
    for user in users_to_delete:
        user.delete()
    users_to_delete = Reviews.objects.filter(id_user=id_const_user)
    for user in users_to_delete:
        user.delete()
    users_to_delete = Albums.objects.filter(id_user=id_const_user)
    id_al = Albums.objects.filter(id_user=id_const_user)
    for i in id_al:
        lst = AlbumList.objects.filter(id_album=i.id_album)
        for j in lst:
            j.delete()
        i.delete()
    users_to_delete = Playlists.objects.filter(id_user=id_const_user)
    id_al = Playlists.objects.filter(id_user=id_const_user)
    for i in id_al:
        lst = PlaylistList.objects.filter(id_album=i.id_playlist)
        for j in lst:
            j.delete()
        i.delete()
    users_to_delete = Songs.objects.filter(id_user=id_const_user)
    for song in users_to_delete:
        song.delete()
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
    rev = Reviews.objects.all().filter(id_song=song_id).values('id_reviewer__login', 'text', 'date', 'id_reviewer', 'id_reviewer_id')
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
        rep = Reposts.objects.filter(id_reposter=id_const_user, id_song=song_id)
        print(rep)
        if rep.count() == 0:
            context = {'song': response, 'reviews': rev, 'title': title, 'albums': albums,
                       'playlists': mixes, 'author': user, 'time': time, "rep": 1}
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


#  готово (возможно)
def delete_song_by_id(request, song_id):
    user_id = Songs.objects.get(id_song=song_id).id_user
    songs_to_delete = AlbumList.objects.filter(id_song=song_id)
    if songs_to_delete is not None:
        for song in songs_to_delete:
            song.delete()
    songs_to_delete = PlaylistList.objects.filter(id_song=song_id)
    if songs_to_delete is not None:
        for song in songs_to_delete:
            song.delete()
    songs_to_delete = Reviews.objects.filter(id_song=song_id)
    if songs_to_delete is not None:
        for song in songs_to_delete:
            song.delete()
    songs_to_delete = Reposts.objects.filter(id_song=song_id)
    if songs_to_delete is not None:
        for song in songs_to_delete:
            song.delete()
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
        context = {"album": res, "title": title, "author": author, "id_const": id_const_user, "id_al": album_id}
    else:
        context = {"album": res, "title": title, "author": author}
    return render(request, 'platform_working/albums_lists.html', context=context)


#  используется
def get_album_by_user_id(request, user_id):
    res = Albums.objects.all().filter(id_user=user_id)
    return res


#  готово
def create_album(request):
    if request.method == 'POST':
        global id_const_user
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            form.cleaned_data['id_user'] = Users.objects.get(id_user=id_const_user)
            form.cleaned_data['date'] = datetime.now().date()
            album = Albums(**form.cleaned_data)
            album.save()
            # print(form.cleaned_data)
            return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
    else:
        form = AddAlbumForm()
    return render(request, 'platform_working/new_album.html', context={'form': form})


#  готово
def create_album_list(request, album_id):
    global id_const_user
    songs = Songs.objects.all().filter(id_user=id_const_user)
    context = {'songs': songs, 'al_id': album_id}
    if request.method == 'POST':
        lst = request.POST.getlist('songs')
        numbers = []
        for song in lst:
            title = Songs.objects.get(id_song=int(song)).song_title
            time = Songs.objects.get(id_song=int(song)).time
            number = int(request.POST['number'])
            for n in numbers:
                if n == number:
                    number = max(numbers) + 1
            if number < 0:
                number = max(numbers) + 1
            numbers.append(number)
            album = Albums.objects.get(id_album=album_id)
            new_album_list = AlbumList(id_album=album, id_song=int(song), number=int(number), time=time,
                                       song_title=title)
            new_album_list.save()

        return HttpResponseRedirect(reverse('platform_working:album_list', args=(album_id,)))
    return render(request, 'platform_working/new_album_list.html', context=context)


def update_album(request, album_id):
    album = Albums.objects.get(id_album=album_id)
    form = UpdateAlbumForm(request.POST or None, instance=album)
    if form.is_valid():
        try:
            form.save()
            return HttpResponseRedirect(reverse('platform_working:album_list', args=(album_id,)))
        except:
            form.add_error(None, 'Ошбика обновления альбома')

    return render(request, 'platform_working/update_album.html', context={'form': form})


# def update_album_list(request, album_id, on_delete, song_id):
#     if on_delete:
#         AlbumList.objects.get(id_album=album_id, id_song=song_id).delete()
#         return HttpResponseRedirect(reverse('platform_working:album_list', args=(album_id,)))


#  готово
def delete_album_by_id(request, album_id):
    AlbumList.objects.all().filter(id_album=album_id).delete()
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
        context = {"title": title, "author": author, "playlist": response, "users": lst, "id_const": id_const_user,
                   "pl_id": playlist_id}
    else:
        context = {"title": title, "author": author, "playlist": response, "users": lst}
    return render(request, 'platform_working/playlists_lists.html', context=context)


# yes
def create_playlist(request):
    if request.method == 'POST':
        global id_const_user
        form = AddPlaylistForm(request.POST)
        if form.is_valid():
            form.cleaned_data['id_user'] = Users.objects.get(id_user=id_const_user)
            playlist = Playlists(**form.cleaned_data)
            playlist.save()
            # print(form.cleaned_data)
            return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
    else:
        form = AddPlaylistForm()
    return render(request, 'platform_working/new_playlist.html', context={'form': form})


# yes
def create_playlist_list(request, playlist_id):
    global id_const_user
    songs = Songs.objects.all()
    context = {'songs': songs, 'pl_id': playlist_id}
    if request.method == 'POST':
        lst = request.POST.getlist('songs')
        numbers = []
        for song in lst:
            title = Songs.objects.get(id_song=int(song)).song_title
            time = Songs.objects.get(id_song=int(song)).time
            author_id = Songs.objects.get(id_song=int(song)).id_user.id_user
            number = int(request.POST['number'])
            for n in numbers:
                if n == number:
                    number = max(numbers) + 1
            if number < 0:
                number = max(numbers) + 1
            numbers.append(number)
            playlist = Playlists.objects.get(id_playlist=playlist_id)
            new_playlist_list = PlaylistList(id_playlist=playlist, id_song=int(song), id_author=author_id,
                                             time=time, number=number, song_title=title)
            new_playlist_list.save()

        return HttpResponseRedirect(reverse('platform_working:playlist_list', args=(playlist_id,)))
    return render(request, 'platform_working/new_playlist_list.html', context=context)


# yes
def update_playlist(request, playlist_id):
    playlist = Playlists.objects.get(id_playlist=playlist_id)
    form = UpdatePlaylistForm(request.POST or None, instance=playlist)
    if form.is_valid():
        try:
            form.save()
            return HttpResponseRedirect(reverse('platform_working:playlist_list', args=(playlist_id,)))
        except:
            form.add_error(None, 'Ошбика обновления плейлиста')

    return render(request, 'platform_working/update_playlist.html', context={'form': form})


# def update_playlist_list(request, playlist_id, song_id):
#     return 1


#  yes
# yes
def delete_playlist_by_id(request, playlist_id):
    PlaylistList.objects.all().filter(id_playlist=playlist_id).delete()
    Playlists.objects.filter(id_playlist=playlist_id).delete()
    return render(request, 'platform_working/all_playlists.html')


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


#  yes
def create_group(request):
    if request.method == 'POST':
        global id_const_user
        form = AddGroupForm(request.POST)
        if form.is_valid():
            creator = Users.objects.get(id_user=id_const_user).login
            user = Users.objects.get(id_user=id_const_user)
            group = Groups(creator=creator, group_title=form.cleaned_data['group_title'],
                           description=form.cleaned_data['description'], id_user=user)
            group.save()
            return HttpResponseRedirect(reverse('platform_working:group_members', args=(group.id_group,)))
    else:
        form = AddGroupForm()
    return render(request, 'platform_working/new_group.html', context={'form': form})


# yes
def update_group(request, group_id):
    group = Groups.objects.get(id_group=group_id)
    form = UpdateAlbumForm(request.POST or None, instance=group)
    if form.is_valid():
        try:
            form.save()
            return HttpResponseRedirect(reverse('platform_working:group_members', args=(group_id,)))
        except:
            form.add_error(None, 'Ошбика обновления сообщества')

    return render(request, 'platform_working/update_album.html', context={'form': form})


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
        if user_id != id_const_user:
            context = {"group": res, "title": title, "user": user, "id_g": 1}
        else:
            context = {"group": res, "title": title, "user": user}

    return render(request, 'platform_working/group_members.html', context=context)


# yes
def create_review_on_user(request, user_id):
    if request.method == 'POST':
        global id_const_user
        form = AddReviewForm(request.POST)
        if form.is_valid():
            date = datetime.now().date()
            reviewer = Users.objects.get(id_user=id_const_user)
            user = Users.objects.get(id_user=user_id)
            review = Reviews(text=form.cleaned_data['text'], date=date, id_reviewer=reviewer,
                             id_user=user, id_song=None)
            review.save()
            return HttpResponseRedirect(reverse('platform_working:profile', args=(user_id,)))
    else:
        form = AddReviewForm()
    return render(request, 'platform_working/new_review.html', context={'form': form, 'user': user_id})


# yes
def create_review_on_song(request, song_id):
    if request.method == 'POST':
        global id_const_user
        form = AddReviewForm(request.POST)
        if form.is_valid():
            date = datetime.now().date()
            reviewer = Users.objects.get(id_user=id_const_user)
            user = Songs.objects.get(id_song=song_id).id_user
            user_id = Users.objects.get(id_user=user.id_user)
            review = Reviews(text=form.cleaned_data['text'], date=date, id_reviewer=reviewer,
                             id_user=user_id, id_song=song_id)
            review.save()
            return HttpResponseRedirect(reverse('platform_working:song', args=(song_id,)))
    else:
        form = AddReviewForm()
    return render(request, 'platform_working/new_review_on_song.html', context={'form': form, 'song': song_id})


# yes
def delete_review_on_user(request, user_id):
    global id_const_user
    Reviews.objects.filter(id_reviewer=id_const_user, id_user=user_id, id_song=None).delete()
    return HttpResponseRedirect(reverse('platform_working:profile', args=(user_id,)))


# yes
def delete_review_on_song(request, song_id):
    global id_const_user
    Reviews.objects.filter(id_reviewer=id_const_user, id_song=song_id).delete()
    return HttpResponseRedirect(reverse('platform_working:song', args=(song_id,)))


# yes
def create_sub(request, user_id, group_id):
    global id_const_user
    follower = Users.objects.get(id_user=id_const_user)
    user = Users.objects.get(id_user=user_id)
    sub = Subscriptions(id_follower=follower, id_group=group_id, id_user=user)
    sub.save()


# yes
def delete_sub_on_user(request, user_id):
    global id_const_user
    Subscriptions.objects.filter(id_user=user_id, id_group=None, id_follower=id_const_user).delete()


# yes
def delete_sub_on_group(request, group_id):
    global id_const_user
    Subscriptions.objects.filter(id_group=group_id, id_follower=id_const_user).delete()


# yes
def create_repost(request, song_id):
    if request.method == 'POST':
        global id_const_user
        form = AddRepostForm(request.POST)
        if form.is_valid():
            reposter = Users.objects.get(id_user=id_const_user)
            user_id = Songs.objects.get(id_song=song_id)
            user = Users.objects.get(id_user=user_id.id_user.id_user)
            repost = Reposts(text=form.cleaned_data['text'], id_song=song_id, id_reposter=reposter, id_user=user)
            repost.save()
            return HttpResponseRedirect(reverse('platform_working:song', args=(song_id,)))
    else:
        form = AddRepostForm()
    return render(request, 'platform_working/new_repost.html', context={'form': form, 'song': song_id})


# yes
def delete_repost(request, song_id):
    global id_const_user
    Reposts.objects.filter(id_song=song_id, id_reposter=id_const_user).delete()
    return HttpResponseRedirect(reverse('platform_working:profile', args=(id_const_user,)))
