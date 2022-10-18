import random
from string import ascii_letters
from .password_validation import validate_password

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (CodeVailForm, EmailValidForm, PasswordValidForm,
                    RegistrForm, loginForm)
from .models import Account, Category, Ip, Likes, News


def validate(nickname):
    return all(map(lambda c: c in ascii_letters, nickname))


def registr(request):
    if request.method == "POST":
        form = RegistrForm(request.POST)
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(email=email):
            messages.error(request, "Пользователь с такой электронной "
                                    "почтой уже существует")
        if User.objects.filter(username=username):
            messages.error(request, "Пользователь с таким именем "
                                    "пользователя уже существует ")
        if password1 != password2:
            messages.error(request, "Пароли отличаются")

        if form.is_valid():
            validate_password(password1)
            message = generate_code()
            send_mail('код подтверждения',
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=True)
            form.save()
            user = User.objects.last()
            login(request, user)
            Account.objects.create(user=User.objects.last(), code=message)
            messages.success(request, f'Мы отправили на вашу почту {email} '
                                      f'сообщение с кодом для подтверждения')
            return redirect('/validate/'+str(user.id))
        else:
           messages.error(request, "Неверный код с картинки")
    else:
        form = RegistrForm()
    return render(request, 'news/registr.html', {"form": form})


def valid(request,user_id):
    if request.method == "POST":
        form = CodeVailForm(request.POST)
        code_response = request.POST.get("code")
        code_base = Account.objects.get(user_id=user_id).code
        if code_base == code_response:
            user = User.objects.get(pk=user_id)
            user.is_staff = True
            user.save()
            login(request, user)#если форма запонена верно войти сразу в этот акк
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect("/")
    else:
        form = CodeVailForm()
    return render(request,"news/vaild.html",{"form":form})


def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def user_login(request):
    if request.method == "POST":
        form = loginForm(data=request.POST)
        captcha = request.POST.get("captcha")
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('/')
        for key, value in form.errors.items():
            messages.error(request, value[0])
    else:
        form = loginForm()
    return render(request, 'news/login.html',{"form":form})

def user_logout(request):
    logout(request)
    messages.error(request, "Вы вышли из аккаунта")
    return redirect('/')



def emailvalid(request):
    if request.method == "POST":
        user = request.user
        form = EmailValidForm(request.POST)
        email_request = request.POST.get("email")
        email_base = user.email
        if form.is_valid():
            if email_base == email_request:
                message = generate_code()
                send_mail('код подтверждения',
                        message,
                        settings.EMAIL_HOST_USER,
                        [email_base],
                        fail_silently=True)
                account = Account.objects.get(user=user)
                account.code = message
                account.save()
                messages.success(request, f'Мы отправили на вашу почту {email_request} '
                                      f'сообщение с кодом для подтверждения')
                return redirect('/validate/' + str(user.id))
        else:
            messages.error(request, "Неверный код с каринки")
    else:
        form = EmailValidForm()
    return render(request,"news/emailvalid.html",{'form':form})


def forgot_password(request):
    if request.method == "POST":
        form = EmailValidForm(request.POST)
        email_request = request.POST.get("email")
        user = User.objects.get(email=email_request)
        if user:
            message = generate_code()
            send_mail('код подтверждения для смены пароля на сайте',
                      message,
                      settings.EMAIL_HOST_USER,
                      [email_request],
                      fail_silently=True)
            account = Account.objects.get(user=user)
            account.code = message
            account.save()
            messages.success(request, f'Мы отправили на вашу почту {email_request} '
                                      f'сообщение с кодом для подтверждения')
            return redirect('/password_value/' + str(user.id))
    else:
        form = EmailValidForm()
    return render(request,"news/forgot_password.html", {"form": form})


def password_value(request,user_id):
    if request.method == "POST":
        code_response = request.POST.get("code")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        form = PasswordValidForm(request.POST)
        code_base = Account.objects.get(user_id=user_id).code
        if code_base == code_response:
            user = User.objects.get(pk=user_id)
            if password1 == password2:
                if len(password1) >7:
                    user.is_staff = True
                    user.set_password(str(password1))
                    user.save()
                    login(request, user)
                    messages.success(request,'Вы успешно поменяли пароль')
                    return redirect("/")
                else:
                    messages.error(request, "Пароль должен быть больше 7 символов")
            else:
                messages.error(request, 'Пароли отличаются')
        else:
            messages.error(request, "Неверный код")
    else:
        form = PasswordValidForm()
    return render(request,"news/password_valid.html", {"form": form})