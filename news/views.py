from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from mysite.settings import *

from .models import Account, Category, Ip, Likes, News


def search(request):
    q = request.GET.get('q')
    all_category = cache.get_or_set("all_category",Category.objects.all(),100)

    if q:
        news = News.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(title_content__icontains=q)
        )
        if not news:
            messages.success(request, f"ничего не найдено по вашему запросу ({q})")
        return render(request, "news/search.html", {
            "news": news,
            "all_category": all_category,
        })
    return redirect('/')


def index(request):
    news = cache.get_or_set("news", News.objects.select_related('autor').all(), 0)
    all_category = cache.get_or_set("all_category", Category.objects.all(), 100)

    paginator = Paginator(news, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/index.html',
                  {
        'news': page_obj,
        'title': 'Список новостей',
        "all_category": all_category,
                  })


# Метод для получения айпи
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip


def detail(request ,pk):
    news = get_object_or_404(News, pk=pk)
    ip = get_client_ip(request)
    obj, created = Ip.objects.get_or_create(ip=ip)
    news.views.add(obj)
    template = 'news/detail.html'

    all_category = cache.get_or_set("all_category",Category.objects.all(),100)

    #if (News.objects.filter(id__gt=pk).first() and News.objects.filter(id__lt=pk).first()):
    #   earliest_news = News.objects.filter(id__lt=pk).first()
    #   latest_news = News.objects.filter(id__gt=pk).first()

    content = {
        "all_category": all_category,
        "five_latest_news": News.objects.order_by('-created_ad')[:5],
        "news":news,
                     }
    return render(request,template,content)


def category(request, category_id):
    all_category = cache.get_or_set("all_category", Category.objects.all(),100)
    category = get_object_or_404(Category, pk=category_id)
    news = category.news_set.select_related('autor').all()

    paginator = Paginator(news, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/category.html',
                  {
    "news": page_obj,
    "category": category,
    "all_category": all_category
                  })



def add_like(request, news_id):
    """Лайкает `obj`.
    """
    if request.user.is_authenticated:
        news_object = get_object_or_404(News, pk=news_id)
        if Likes.objects.filter(news=news_object.id, user=request.user):
            Likes.objects.filter(
                news=news_object.id, user=request.user
            ).delete()
            return render(request, "news/detail.html",
                          {
                "category": Category.objects.all(),
                "five_latest_news": News.objects.order_by('-created_ad')[:5],
                "news": news_object,
                          })
        else:
            like = Likes.objects.get_or_create(news=news_object, user=request.user)
            return render(request,"news/detail.html",
                          {
                "like": like,
                "category": Category.objects.all(),
                "five_latest_news": News.objects.order_by('-created_ad')[:5],
                "news":news_object,
                          })
    else:
        return redirect('/login/')
