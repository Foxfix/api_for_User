from django import forms 
from django.contrib.auth import (
        authenticate,
        get_user_model,
        login,
        logout,
    )

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Нет такого юзера")
            if not user.check_password(password):
                raise forms.ValidationError("Не корректный пароль")
            if not user.is_active:
                raise forms.ValidationError("Пользователь не активен")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    passport_number = forms.CharField(max_length=120)
    email = forms.EmailField() 
    is_active = False

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'passport_number',
            'username',
        ]

        def save(self, commit=True):
            user = super(UserRegisterForm, self).save(commit=False)
            user.username = self.cleaned_data['email']
            user.email = self.cleaned_data['email']
            if commit:
                user.is_active = False
                user.save()
            return user



