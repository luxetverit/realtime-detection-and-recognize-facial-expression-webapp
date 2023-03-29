from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import cv2
import numpy as np
from django.views.decorators import gzip
from pathlib import Path
from .models import Counseling
from django.contrib import messages
from .forms import CounselingForm
from django.views import generic
from .models import Counseling, DetectedEmotions


def index(request):
    return render(request, 'webcam/camindex.html')


def socket(request):
    return render(request, 'webcam/socket.html')





class CounselingListView(generic.ListView):
    model = Counseling
    template_name = 'webcam/counseling_list.html'
    context_object_name = 'counseling_list'

class CounselingDetailView(generic.DetailView):
    model = Counseling
    template_name = 'webcam/counseling_detail.html'
    context_object_name = 'counseling'


def counseling_add(request):
    if request.method == 'POST':
        form = CounselingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Counseling session added successfully.')
            return redirect('counseling_list')
    else:
        form = CounselingForm()
    return render(request, 'webcam/counseling_form.html', {'form': form})



def counseling_edit(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    if request.method == 'POST':
        form = CounselingForm(request.POST, request.FILES, instance=counseling)
        if form.is_valid():
            form.save()
            messages.success(request, 'Counseling session updated successfully.')
            return redirect('counseling_detail', pk=counseling.pk)
    else:
        form = CounselingForm(instance=counseling)
    return render(request, 'webcam/counseling_form.html', {'form': form})



def counseling_delete(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    counseling.delete()
    messages.success(request, 'Counseling session deleted successfully.')
    return redirect('counseling_list')































# def counseling_list(request):
#     userid = request.GET.get('username')

#     counselings = Counseling.objects.all()

#     if userid:
#         counselings = counselings.filter(userid=userid)



#     return render(request, 'webcam/counseling_list.html', {'counselings': counselings})



# def counseling_detail(request, pk):
#     counseling = get_object_or_404(Counseling, pk=pk)
#     return render(request, 'counseling/counseling_detail.html', {'counseling': counseling})





