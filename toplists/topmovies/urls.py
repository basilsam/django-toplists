from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=True)),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('popular-movies/', views.popular_movies, name='popular-movies'),
    path('top-rated/', views.top_rated, name='top-rated'),
    path('my-list/', views.my_list, name='my-list'),
    path('add-movie/', views.add_movie, name='add-movie'),
    path('delete-movie/', views.delete_movie, name='delete-movie'),
    path('search/', views.search, name="search"),
    path('account/', views.account, name="account"),
]