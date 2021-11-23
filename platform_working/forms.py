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
