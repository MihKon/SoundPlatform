from django import forms
from django.core.exceptions import ValidationError
from .models import *


class RegisterForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = Users
        fields = '__all__'
        choices = [(i, i) for i in range(12, 100)]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'age': forms.Select(choices=choices, attrs={'class': 'form-select'}),
            'image': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        users = Users.objects.all().filter(email=self.cleaned_data['email']).count()
        if users != 0:
            raise ValidationError('Пользователь с такой почтой уже существует')

        return self.cleaned_data['email']

    def clean_login(self):
        users = Users.objects.all().filter(login=self.cleaned_data['login']).count()
        if users != 0:
            raise ValidationError('Пользователь с таким логином уже существует')

        return self.cleaned_data['login']


class LoginForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        users = Users.objects.all().filter(email=self.cleaned_data['email']).count()
        if users == 0:
            raise ValidationError('Неверные данные')

        return self.cleaned_data['email']

    def clean_password(self):
        users = Users.objects.all().filter(password=self.cleaned_data['password']).count()
        if users == 0:
            raise ValidationError('Неверный пароль')

        return self.cleaned_data['password']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['image', 'email', 'password']
        widgets = {
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class AddSongForm(forms.ModelForm):

    class Meta:
        model = Songs
        fields = '__all__'
        widgets = {
            'song_title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'})
        }


class UpdateSongForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = ['image', 'genre', 'file', 'song_title']
        widgets = {
            'song_title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddAlbumForm(forms.ModelForm):

    class Meta:
        model = Albums
        fields = ['album_title', 'genre', 'date', 'description', 'number_of_songs']
        widgets = {
            'album_title': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_songs': forms.NumberInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
