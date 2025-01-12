from django.http import HttpResponse
from django.shortcuts import render

def play(request):
    return render(request, 'main/play.html')