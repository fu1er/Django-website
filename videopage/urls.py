from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'videopage'
urlpatterns = [
    path('home/', views.mainpage, name='main'),
    path('authors/', views.authorpage, name='authors'),
    path('search/', views.searchpage, name='search'),
    path('home/<int:video_id>/', views.videodetails, name='hvideo'),
    path('authors/<int:author_id>/', views.authordetails, name='adetails'),
    path('authors/<int:author_id>/<int:video_id>/', views.videodetailsfromauthor, name='avideo'),
    path('search/result/', views.search_result, name='result'),
]