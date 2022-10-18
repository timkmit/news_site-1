from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import imgForm
from .models import News
from .utils import LoginIs_StaffMixin


class NewsDeleteView(LoginIs_StaffMixin,DeleteView):
    login_url = '/'
    model = News
    template_name = 'news/del.html'
    success_url = '/'

class NewsUpdateView(LoginIs_StaffMixin,UpdateView):
    login_url = '/'
    model = News
    template_name = 'news/create.html'
    form_class = imgForm

class NewsCreate(LoginIs_StaffMixin,CreateView):
    login_url = '/'
    # Модель куда выполняется сохранение
    model = News
    # Класс на основе которого будет валидация полей
    form_class = imgForm
    # Выведем все существующие записи на странице
    extra_context = {'news': News.objects.all()}
    # Шаблон с помощью которого
    # будут выводиться данные
    template_name = 'news/create.html'
    # На какую страницу будет перенаправление
    # в случае успешного сохранения формы
    success_url = '/'
    ##добавляет необязательное поле autor к News
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.autor = self.request.user
        self.object.save()
        messages.success(self.request, 'Вы успешно добавили новость')
        return super().form_valid(form)