from django.db import connection
from django.shortcuts import render
import datetime
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from app.models import Question
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


# Create your views here.

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


def index(request):
    return render(request, 'index.html')

def demo(request):
    return render(request, 'demo.html')

def service(request):
    return render(request, 'service.html')

def profile(request):
    return render(request, 'profile.html')

def userinfo(request):
    return render(request, 'userinfo.html')

def login(request):
    return render(request, 'login.html')

def password(request):
    return render(request, 'password.html')

def signup(request):
    return render(request, 'signup.html')

# chartjs
class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

