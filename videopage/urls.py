from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'videopage'
urlpatterns = [
    path('', views.mainpage, name='main'),
    path('authors/', views.authorpage, name='authors'),
    path('search/', views.searchpage, name='search'),
    path('<int:video_id>/', views.videodetials, name='detials'),
    path('authors/<int:author_id>/', views.authordetials, name='adetials'),
    path('search/result/', views.search_result, name='result'),
]