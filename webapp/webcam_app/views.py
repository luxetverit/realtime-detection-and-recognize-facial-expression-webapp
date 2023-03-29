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

def socket(request):
    model= Counseling
    return render(request, 'webcam/socket.html')



def counseling_list(request):
    userid = request.GET.get('username')

    counselings = Counseling.objects.all()

    if userid:
        counselings = counselings.filter(userid=userid)



    return render(request, 'webcam/counseling_list.html', {'counselings': counselings})



def counseling_detail(request, pk):
    counseling = get_object_or_404(Counseling, pk=pk)
    return render(request, 'counseling/counseling_detail.html', {'counseling': counseling})





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