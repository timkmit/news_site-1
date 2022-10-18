import django.views.generic
from django.urls import path

from . import auth, autor, views

app_name = 'news'
urlpatterns = [
    path('likes/<int:news_id>/', views.add_like, name='add'),
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('category/<int:category_id>', views.category, name='category'),
    path('create/', autor.NewsCreate.as_view(), name='create'),
    path('<int:pk>/update', autor.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/del', autor.NewsDeleteView.as_view(), name='delete'),
    path('search/', views.search, name='search'),
    path('login/', auth.user_login, name='account_login'),
    path('register/', auth.registr, name='account_signup'),
    path('logout/', auth.user_logout, name='account_logout'),
    path('validate/<int:user_id>/', auth.valid, name="account_validate"),
    path('validate/', auth.emailvalid, name="emailvalid"),
    path('forgot_password', auth.forgot_password, name="forgot_password"),
    path('password_value/<int:user_id>', auth.password_value, name="password_value"),
]
