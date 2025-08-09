from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    # return render(request, 'main/index.html')
    return render(request, 'accounts/test.html')

def main(request):
    # return render(request, 'main/index.html')
    return render(request, 'main/index.html')


