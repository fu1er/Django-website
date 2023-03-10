from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from .models import Author, Videoinfo
from django.db.models import Q
import time
def mainpage(request):
    videos = Videoinfo.objects.only(
        'video_name', 'cover'
    )
    paginator = Paginator(videos, 60)
    page = request.GET.get('page', 1)
    try:  
        page = int(page)
    except :
        page = 1
    if page > paginator.num_pages:
        page = paginator.num_pages
    page_obj = paginator.get_page(page)
    
    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=1, on_ends=2)
    context = {
        'page_obj': page_obj, 'paginator': paginator, 'is_paginated': is_paginated, 'page_range': page_range
    }
    return render(request, 'videopage/mainpage.html', context)

def videodetails(request, video_id):
    video = Videoinfo.objects.select_related('author').filter(id=video_id).first()
    video.brief = video.brief[2:len(video.brief)-2]
    com_list = video.comment[2:len(video.comment)-2].split("', '")
    if video:
        return render(request, 'videopage/videodetails.html', {'video': video, 'com_list': com_list})
    else:
        return Http404('视频不存在哦')

def videodetailsfromauthor(request, author_id, video_id):
    video = Videoinfo.objects.select_related('author').filter(id=video_id).first()
    video.brief = video.brief[2:len(video.brief)-2]
    com_list = video.comment[2:len(video.comment)-2].split("', '")
    if video:
        return render(request, 'videopage/videodetails.html', {'video': video, 'com_list': com_list})
    else:
        return Http404('视频不存在哦')

def authorpage(request):
    authors = Author.objects.only(
        'name', 'photo'
    )
    paginator = Paginator(authors, 60)
    page = request.GET.get('page', 1)
    try:  
        page = int(page)
    except :
        page = 1
    if page > paginator.num_pages:
        page = paginator.num_pages
    page_obj = paginator.get_page(page)

    is_paginated = True if paginator.num_pages>1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=1, on_ends=2)
    context = {
        'page_obj': page_obj, 'paginator': paginator, "is_paginated": is_paginated, 'page_range':page_range
    }
    return render(request, 'videopage/authorspage.html', context)

def authordetails(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    author.describe = author.describe[2:len(author.describe)-2]
    if author:
        return render(request, 'videopage/authordetails.html', {'author':author})
    else:
        return Http404('作者不存在哦')

def searchpage(request):
    return render(request, 'videopage/searchpage.html',)

def search_result(request):
    md = request.GET.get('md', 'none')
    word = request.GET.get('info', 'none')
    # print(md, word)
    if md == 'author' :
        time_start=time.time()
        result = Author.objects.all().filter(Q(name__contains=word)| Q(describe__contains=word))
        if result:
            md_r = "md="+md
            word_r = "info="+word
            paginator = Paginator(result, 40)
            page = request.GET.get('page', 1)
            try:  
                page = int(page)
            except :
                page = 1
            if page > paginator.num_pages:
                page = paginator.num_pages
            page_obj = paginator.get_page(page)
    
            is_paginated = True if paginator.num_pages > 1 else False
            page_range = paginator.get_elided_page_range(page, on_each_side=1, on_ends=2)
            time_end=time.time()
            time_used = round(time_end-time_start,3)
            context = {
                'page_obj': page_obj, 'paginator': paginator, 'is_paginated': is_paginated, 'page_range': page_range, 'md_r':md_r, 'word_r':word_r, 'time_used': time_used
            }
            return render(request, 'videopage/authorresult.html', context)
        else:
            return render(request, 'videopage/noresult.html',)
    elif md == 'video' :
        time_start=time.time()
        result = Videoinfo.objects.all().filter(Q(video_name__contains=word)| Q(brief__contains=word))
        if result:
            md_r = "md="+md
            word_r = "info="+word
            paginator = Paginator(result, 40)
            page = request.GET.get('page', 1)
            try:  
                page = int(page)
            except :
                page = 1
            if page > paginator.num_pages:
                page = paginator.num_pages
            page_obj = paginator.get_page(page)
    
            is_paginated = True if paginator.num_pages > 1 else False
            page_range = paginator.get_elided_page_range(page, on_each_side=1, on_ends=2)
            time_end=time.time()
            time_used = round(time_end-time_start,3)
            context = {
                'page_obj': page_obj, 'paginator': paginator, 'is_paginated': is_paginated, 'page_range': page_range, 'md_r':md_r, 'word_r':word_r, 'time_used': time_used
            }
            return render(request, 'videopage/videoresult.html', context)
        else:
            return render(request, 'videopage/noresult.html')