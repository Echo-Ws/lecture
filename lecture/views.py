from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Lecture

# Create your views here.


def index(request):
    return render(request, 'lecture/index.html')


def content(request):
    o = request.GET.get('o')
    if not o:
        o = 'time'

    if o[0].isalpha():
        a = '-'
    else:
        a = ''

    q = request.GET.get('q')
    if q:
        try:
            contact_list = Lecture.objects.filter(title__icontains=q)
        except Lecture.DoesNotExist:
            return render(request, 'lecture/index.html', {'message': a,})
    else:
        contact_list = Lecture.objects.order_by(o)

    paginator = Paginator(contact_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
        print contacts
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'lecture/content.html', {
        'lecture_list': contacts,
        'message': a,
    })