from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import (DateTimeInput, FileInput, ModelForm, Select,
                          Textarea, TextInput)
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget

from .models import Category, News


class PasswordValidForm(forms.Form):
    code = forms.CharField(max_length=50, label='Код подтвержения',
                           widget=forms.TextInput(attrs={'class': 'form-control w-25'}))

    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(
        attrs={"class": "form-control w-25",
               "placeholder": "Пароль"
               }
    ))
    password2 = forms.CharField(label='Пароль повторно',widget=forms.PasswordInput(
        attrs={"class": "form-control w-25",
               "placeholder": "Подтверждение пароля",
               }
    ))


class EmailValidForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control w-25",
               "placeholder": "E-mail"
               }
    ))
    captcha = CaptchaField(error_messages={'invalid': 'Неверный код с картинки'},
        widget=CaptchaTextInput(
        attrs={"placeholder": "Код с картинки"}
    ))

class CodeVailForm(forms.Form):
    code = forms.CharField( max_length=50, label='Код подтвержения',
                           widget=forms.TextInput(attrs={'class': 'form-control w-25'}))


class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control w-25",
               "placeholder": "Имя Пользователя"
               }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control ml-25 w-25",
            "placeholder": "Пароль"}
    ))
    captcha = CaptchaField(error_messages={'invalid': 'Неверный код с картинки'},
        widget=CaptchaTextInput(
        attrs={"placeholder": "Код с картинки"}
    ))
    error_messages = {
        'invalid_login': ("Неверный логин или пароль"),
        'inactive': ("This account is inactive."),
        "error_message" : ("Неверный код с картинки")

    }


class RegistrForm(UserCreationForm ):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control w-25",
               "placeholder":"Имя Пользователя"}

    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control w-25",
               "placeholder":"Пароль"
               }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control w-25",
               "placeholder":"Подтверждение пароля",
               }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control w-25",
               "placeholder":"E-mail"
               }
    ))
    captcha = CaptchaField(widget=CaptchaTextInput(
        attrs={"placeholder": "Код с картинки"}
    ))

    class Meta:
        model = User
        fields = {"username", "email", "password1", "password2"}


class SomeForm(forms.Form):
    content = forms.CharField(widget=SummernoteWidget(
        attrs={'summernote': {'width': '50%', 'height': '400px'}}))  # instead of forms.Textarea


class imgForm(ModelForm):
    class Meta:
        # Название модели на основной
        # которой создается форма
        model = News
        # Включаем все поля с модели в форму
        fields = [
            "title",
            "title_content",
            "content",
            "created_ad",
            "photo",
            "category",
            "key_word"
        ]

        widgets = {
            'content': SummernoteWidget(attrs={
                'summernote': {'width': '99.7%', 'height': '600px'}
            }),
            'title': TextInput(attrs={
                'class': 'form-control  w-25 ',
                'placeholder': 'название статьи'
            }),
            "title_content": TextInput(attrs={
                'class': 'form-control  w-75 ',
                'placeholder': 'завлекающая информация'
            }),
            """"content": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'текст статьи'
            }),"""
            "created_ad": DateTimeInput(attrs={
                'class': 'form-control ',
            }),
            "photo": FileInput(attrs={
                'class': 'form-control  w-25',
            }),
            "category" : Select({
                'class': 'form-control w-25',
            }),


        }

