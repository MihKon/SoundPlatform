# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AlbumList(models.Model):
    id_album = models.OneToOneField('Albums', models.DO_NOTHING, db_column='id_album', primary_key=True)
    id_song = models.IntegerField()
    number = models.IntegerField()
    time = models.TimeField(blank=True, null=True)
    song_title = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'album_list'
        unique_together = (('id_album', 'id_song'),)


class Albums(models.Model):
    id_album = models.AutoField(primary_key=True)
    album_title = models.CharField(max_length=50)
    number_of_songs = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'albums'


class Groups(models.Model):
    id_group = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=50)
    group_title = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'groups'


class PlaylistList(models.Model):
    id_playlist = models.OneToOneField('Playlists', models.DO_NOTHING, db_column='id_playlist', primary_key=True)
    id_song = models.IntegerField()
    id_author = models.IntegerField()
    time = models.TimeField(blank=True, null=True)
    number = models.IntegerField()
    song_title = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'playlist_list'
        unique_together = (('id_playlist', 'id_song'),)


class Playlists(models.Model):
    id_playlist = models.AutoField(primary_key=True)
    playlist_title = models.CharField(max_length=40)
    time = models.TimeField(blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'playlists'


class Reposts(models.Model):
    id_repost = models.AutoField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    id_song = models.IntegerField()
    id_reposter = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_reposter', related_name='reposters')
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'reposts'


class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    text = models.TextField()
    date = models.DateField()
    id_reviewer = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_reviewer', related_name='reviewers')
    id_song = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'reviews'


class Songs(models.Model):
    id_song = models.AutoField(primary_key=True)
    song_title = models.CharField(max_length=40)
    genre = models.CharField(max_length=30, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    file = models.TextField()
    time = models.TimeField()
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'songs'

    def __str__(self):
        return self.song_title


class Subscriptions(models.Model):
    id_subscription = models.AutoField(primary_key=True)
    id_follower = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_follower', related_name='followers')
    id_group = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'subscriptions'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.TextField()
    age = models.IntegerField()
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
