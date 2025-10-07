from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'accounts/test.html')

def main(request):
    return render(request, 'main/index.html')

def about_game(request):
    return render(request, 'about_game/about_game.html')

def achievements(request):

    return render(request, 'achievements/achievements.html')


