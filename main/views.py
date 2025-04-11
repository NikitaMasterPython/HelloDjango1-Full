from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.http import  JsonResponse

# counter = 10
#
# def play (request):
#     global counter
#     if request.method == 'POST':
#         counter +=10
#         return redirect ('play')
#     return render (request, 'play/play.html',{'counter': counter})
#
def index(request):
    return render(request, 'main/index.html')



#
# def play(request):
#     data = {
#         'Hit_points': HP,
#
#         'Damage': Damage,
#
#         'counter': counter,
#     }
#     return render(request, 'play/play.html',data)
# HP=100
# Damage=1
# Hill=1
# change_hp=HP-1
# change_hp-=-1

