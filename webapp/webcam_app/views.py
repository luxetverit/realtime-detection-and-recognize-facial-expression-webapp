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


def index(request):
    return render(request, 'webcam/camindex.html')







class CounselingListView(generic.ListView):
    model = Counseling
    template_name = 'webcam/counseling_list.html'
    context_object_name = 'counseling_list'

class CounselingDetailView(generic.DetailView):
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
        


    
def counseling_add(request):
    if request.method == 'POST':
        form = CounselingForm(request.POST, request.FILES)
        if form.is_valid():
            counseling = form.save(commit=False)
            counseling.user  = request.user
            counseling.save()

            if request.POST.get('realtime_true_false') == 'on':
                return redirect('webcam:realtime', pk=counseling.pk)
            else:
                messages.success(request, '상담 세션 추가 완료.')
                return redirect('webcam:counseling_list')
    else:
        form = CounselingForm()
    return render(request, 'webcam/counseling_form.html', {'form': form})



def counseling_edit(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
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



def counseling_delete(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    counseling.delete()
    messages.success(request, '상담 세션 제거 완료.')
    return redirect('webcam:counseling_list')







def socket(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    detected_emotions = counseling.detectedemotions
    context = {
        'counseling': counseling,
        'detected_emotions': detected_emotions,
    }
    return render(request, 'webcam/socket.html', context)























# def counseling_list(request):
#     userid = request.GET.get('username')

#     counselings = Counseling.objects.all()

#     if userid:
#         counselings = counselings.filter(userid=userid)



#     return render(request, 'webcam/counseling_list.html', {'counselings': counselings})



# def counseling_detail(request, pk):
#     counseling = get_object_or_404(Counseling, pk=pk)
#     return render(request, 'counseling/counseling_detail.html', {'counseling': counseling})





