from django.contrib.auth.decorators import login_required
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


# def get_player_status(request):
#     if request.user.is_authenticated:
#         try:
#             player_status = status.objects.get(user=request.user)
#             return JsonResponse({
#                 'success': True,
#                 'hp': player_status.status_HP,
#                 'money': player_status.status_Money,
#                 'loyalty': player_status.status_Loyalty,
#                 'herbs': player_status.status_Herbs,
#                 'Samogon': player_status.status_Samogon,
#                 'Poison': player_status.status_Poison,
#                 'Fish': player_status.status_Fish,
#                 'Jewelry': player_status.status_Jewelry
#             })
#         except status.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Status not found'})
#     return JsonResponse({'success': False, 'error': 'User not authenticated'})

@login_required
def mybag(request):
    # Получаем статус текущего пользователя
    player_status = status.get_default_status(request.user)
    return render(request, 'mybag/bag.html', {
        'player_status': player_status
    })

def map_0(request):
    # Получаем статус текущего пользователя
    player_status = status.get_default_status(request.user)
    return render(request, 'map/map_0.html', {
        'player_status': player_status
    })
