from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import event


# from django.http import  JsonResponse



def play (request):

    return render (request, 'play/play.html')

def play_next (request, event_id):
    Event = get_object_or_404(event, id=event_id)
    return render(request,'play/play.html', {'event': Event})

def event_part_2 (request, event_id):
    Event = get_object_or_404(event, id=event_id)
    return render(request,'play/play.html', {'event': Event})


