from django.db import connection
from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now

from app.models import Question


def index(request):
    data = {
        'userId': 'dooho',
        'name': '함두호'
    }

    return JsonResponse(data)
    #return render(request, 'index.html', {'page': 'index'})

def question_insert(request):
    subject = '제목제목'
    content = '내용내용내용내용'
    author = 'dooho'
    pub_date = now
    #1 MODEL
    question = Question(subject=subject, content=content, author=author, pub_date=pub_date)
    question.save()

    #2 QUERY
    cursor = connection.cursor()
    result = cursor.execute(f"INSERT INTO question(subject, content, author, pub_date) VALUE ('{subject}','{content}','{author}', now())")
    data = {
        'userId': 'dooho',
        'name': '함두호'
    }

    return JsonResponse(data)


#def question_select(request):
#