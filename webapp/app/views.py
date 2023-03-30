from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Posts, Comments
from .forms import PostsForm, CommentsForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


# def login(request):
#     return render(request, 'login.html')


# 게시판 페이지 설정
def index(request):
    return render(request, 'index.html')

def qna(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    Posts_list = Posts.objects.order_by('-create_at') # 생성한 날짜 보이기
    if kw:
        Posts_list = Posts_list.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(Comments__content__icontains=kw) |  # 답변 내용 검색
            Q(user__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(Comments__user__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(Posts_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'posts_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'question_list.html', context)

def detail(request, board_id):
    posts = get_object_or_404(Posts, pk=board_id)
    context = {'posts': posts}
    return render(request, '../templates/question_detail.html', context)

# required 로그인하지 않을시 로그인 화면으로 이동하게 됨
@login_required(login_url='account:login_view') # 당사자만 접근 가능하게 설정
def Comments_create(request, Posts_id):
    """
    QnA 답변등록
    """
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            Comments = form.save(commit=False)
            Comments.user = request.user  # user 속성에 로그인 계정 저장
            Comments.create_at = timezone.now()
            Comments.Posts = Posts
            Comments.save()
            return redirect('app:detail', Posts_id=Posts.board_id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'Posts': Posts, 'form': form}
    return render(request, 'app/posts_detail.html', context)

@login_required(login_url='account:login_view')
def Posts_create(request):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            Posts = form.save(commit=False)
            Posts.user = request.user  # user 속성에 로그인 계정 저장 
            Posts.create_at = timezone.now()
            Posts.save()
            return redirect('app:index')
    else:
        form = PostsForm()
    context = {'form': form}
    return render(request, '../templates/question_form.html', context)
@login_required(login_url='account:login_view')
def Posts_modify(request, Posts_id):
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.user != Posts.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('app:detail', Posts_id=Posts.board_id)
    if request.method == "POST":
        form = PostsForm(request.POST, instance=Posts)
        if form.is_valid():
            Posts = form.save(commit=False)
            Posts.modify_date = timezone.now()  # 수정일시 저장
            Posts.save()
            return redirect('app:detail', Posts_id=Posts.board_id)
    else:
        form = PostsForm(instance=Posts)
    context = {'form': form}
    return render(request, 'app/Posts_form.html', context)
@login_required(login_url='account:login_view')
def Posts_delete(request, Posts_id):
    Posts = get_object_or_404(Posts, pk=Posts_id)
    if request.user != Posts.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('app:detail', Posts_id=Posts.board_id)
    Posts.delete()
    return redirect('app:index')
@login_required(login_url='account:login_view')
def Comments_modify(request, Comments_id):
    Comments = get_object_or_404(Comments, pk=Comments_id)
    if request.user != Comments.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('app:detail', Posts_id=Comments.Posts.board_id)
    if request.method == "POST":
        form = CommentsForm(request.POST, instance=Comments)
        if form.is_valid():
            Comments = form.save(commit=False)
            Comments.modify_date = timezone.now()
            Comments.save()
            return redirect('app:detail', Posts_id=Comments.Posts.board_id)
    else:
        form = CommentsForm(instance=Comments)
    context = {'Comments': Comments, 'form': form}
    return render(request, 'app/Comments_form.html', context)
@login_required(login_url='account:login_view')
def Comments_delete(request, Comments_id):
    Comments = get_object_or_404(Comments, pk=Comments_id)
    if request.user != Comments.user:
        messages.error(request, '삭제권한이 없습니다')
    else:
        Comments.delete()
    return redirect('app:detail', Posts_id=Comments.Posts.board_id)


def demo(request):
    return render(request, 'demo.html')
def service(request):
    return render(request, 'service.html')



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


line_chart = TemplateView.as_view(template_name='../demo.html')
line_chart_json = LineChartJSONView.as_view()

