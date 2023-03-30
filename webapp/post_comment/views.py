from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import BoardPost, BoardComment
from .forms import BoardPostForm, BoardCommentForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView




# 게시판 페이지 설정
def index(request):
    return render(request, 'index.html')

def post_list(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    Posts_list = BoardPost.objects.order_by('-create_at') # 생성한 날짜 보이기
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
    return render(request, 'boardpost_list.html', context)

def detail(request, pk):
    posts = get_object_or_404(BoardPost, pk=pk)
    form=BoardCommentForm()
    context = {'posts': posts,'form':form}
    return render(request, 'boardpost_detail.html', context)






@login_required(login_url='account:login_view')
def posts_create(request):
    if request.method == 'POST':
        form = BoardPostForm(request.POST)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.user = request.user  # user 속성에 로그인 계정 저장 
            posts.save()
            return redirect('app:detail',posts.pk)
    else:
        form = BoardPostForm()
    context = {'form': form}
    return render(request, 'boardpost_form.html', context)




@login_required(login_url='account:login_view')
def posts_modify(request, pk):
    posts = get_object_or_404(BoardPost, pk=pk)
    if request.user != posts.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('app:detail', pk=posts.pk)
    if request.method == "POST":
        form = BoardPostForm(request.POST, instance=posts)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.save()
            return redirect('app:detail', pk=posts.pk)
    else:
        form = BoardPostForm(instance=posts)
    context = {'form': form}
    return render(request, 'boardpost_form.html', context)




@login_required(login_url='account:login_view')
def posts_delete(request, pk):
    posts = get_object_or_404(BoardPost, pk=pk)
    if request.user != posts.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('app:detail', pk=posts.pk)
    posts.delete()
    return redirect('app:index')



# required 로그인하지 않을시 로그인 화면으로 이동하게 됨
@login_required(login_url='account:login_view') # 당사자만 접근 가능하게 설정
def comments_create(request, pk):
    """
    QnA 답변등록
    """
    boardpost  = get_object_or_404(BoardPost, pk=pk)
    
    
    if request.method == "POST":
        form = BoardCommentForm(request.POST)
        
        if form.is_valid():
            comments = form.save(commit=False)
            comments.user = request.user  # user 속성에 로그인 계정 저장
            comments.boardpost = boardpost 
            comments.save()
            return redirect('app:detail', pk=boardpost.pk)
    else:
        form = BoardCommentForm()
        
    context = {'Posts': boardpost, 'form': form}
    return render(request, 'boardpost_detail.html', context)




@login_required(login_url='account:login_view')
def comments_modify(request, pk):
    comments = get_object_or_404(BoardComment, pk=pk)
    if request.user != comments.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('app:detail', pk=comments.boardpost.pk)
    if request.method == "POST":
        form = BoardCommentForm(request.POST, instance=comments)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.save()
            return redirect('app:detail', pk=comments.boardpost.pk)
    else:
        form = BoardCommentForm(instance=comments)
    context = {'Comments': comments, 'form': form}
    return render(request, 'comments_form.html', context)




@login_required(login_url='account:login_view')
def comments_delete(request, pk):
    comments = get_object_or_404(BoardComment, pk=pk)
    boardpost=comments.boardpost
    if request.user != comments.user:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comments.delete()
    return redirect('app:detail', pk=boardpost.pk)


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


line_chart = TemplateView.as_view(template_name='demo.html')
line_chart_json = LineChartJSONView.as_view()

