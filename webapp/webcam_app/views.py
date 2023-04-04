from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import cv2
import numpy as np
from django.views.decorators import gzip
from pathlib import Path
from .models import Counseling,DetectedEmotions
from django.contrib import messages
from .forms import CounselingForm,CounselingEditForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .videotake import videocheck


def index(request):
    return render(request, 'webcam/camindex.html')


class CounselingListView(LoginRequiredMixin,generic.ListView):
    model = Counseling
    template_name = 'webcam/counseling_list.html'
    context_object_name = 'counseling_list'
    
    def get_queryset(self):
        return Counseling.objects.filter(user=self.request.user)
    

class CounselingDetailView(LoginRequiredMixin,generic.DetailView):
    model = Counseling
    template_name = 'webcam/counseling_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counseling = self.get_object()
        context["counseling"] = counseling
        try:
            context["detectedemotion"] = DetectedEmotions.objects.get(pk=counseling.pk)
        except DetectedEmotions.DoesNotExist:
            context["detectedemotion"] = None
        return context 
        

@login_required(login_url='account:login')   
def counseling_add(request):
    if request.method == 'POST':
        form = CounselingForm(request.POST, request.FILES)
        if form.is_valid():
            counseling = form.save(commit=False)
            counseling.user  = request.user
            
            if request.FILES :
                file = request.FILES['storage_data']
                file_name = file.name
                with open('media/cam'+file_name, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                counseling.storage_data = file_name
            counseling.save()

            if request.POST.get('realtime_true_false') == 'on':
                return redirect('webcam:realtime', pk=counseling.pk)
            else :
                # request.FILES['storage_data']:
                # video_path=counseling.storage_data.path
                # print(video_path)
                # messages.success(request, '상담 세션 추가 완료.')
                return redirect('webcam:counseling_detail', pk=counseling.pk) 
    else:
        form = CounselingForm()
    return render(request, 'webcam/counseling_form.html', {'form': form})


@login_required(login_url='account:login')
def counseling_edit(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    if request.user != counseling.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('webcam:counseling_list', pk=counseling.pk)
    
    if request.method == 'POST':
        form = CounselingEditForm(request.POST, request.FILES, instance=counseling)
        if form.is_valid():
            updated_counseling = form.save(commit=False)
            updated_counseling.user = request.user
            updated_counseling.save()
            messages.success(request, '상담 세션 업데이트 완료.')
            return redirect('webcam:counseling_detail', pk=counseling.pk)
    else:
        form = CounselingEditForm(instance=counseling)
    return render(request, 'webcam/counseling_form.html', {'form': form})


@login_required(login_url='account:login')
def counseling_delete(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    if request.user != counseling.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('webcam:counseling_detail', pk=counseling.pk)
    else: 
        counseling.delete()
        messages.success(request, '상담 세션 제거 완료.')
    return redirect('webcam:counseling_list')


@login_required(login_url='account:login')
def socket(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    detected_emotions = counseling.detectedemotions
    context = {
        'counseling': counseling,
        'detected_emotions': detected_emotions,
    }
    return render(request, 'webcam/socket.html', context)

























