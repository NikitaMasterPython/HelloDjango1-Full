from django.shortcuts import render
from play.models import status  # Импорт модели из приложения play

def get_player_status():
    status_obj, _ = status.objects.get_or_create(
        pk=1,
        defaults={
            'status_HP': 100,
            'status_Money': 50,
            'status_Loyalty': 0
        }
    )
    return status_obj

def mybag(request):
    player_status = get_player_status()
    return render(request, 'mybag/bag.html', {
        'player_status': player_status
    })



