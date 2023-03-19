from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    data = {
        'userId': 'dooho',
        'name': '함두호'
    }

    return JsonResponse(data)
    #return render(request, 'index.html', {'page': 'index'})
