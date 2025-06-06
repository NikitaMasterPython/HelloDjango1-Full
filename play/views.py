from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import event
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import event, status  # Добавляем импорт модели status
import random


def get_random_event_id():
    """Получение случайного ID события"""
    event_ids = list(event.objects.values_list('id', flat=True))
    return random.choice(event_ids) if event_ids else None


def play(request):
    """Главная страница игры"""
    random_id = get_random_event_id()
    if random_id:
        return redirect('play_next', event_id=random_id)
    return render(request, 'play/play.html')


def play_next(request, event_id):
    """Обработка конкретного события"""
    event_obj = get_object_or_404(event, id=event_id)
    player_status, _ = status.objects.get_or_create(pk=1)

    return render(request, 'play/play.html', {
        'event': event_obj,
        'player_status': player_status,
        'consequence': None,
        'show_event_text': True

    })
def get_player_status():
    """Получаем или создаем статус игрока с значениями по умолчанию"""
    status_obj, created = status.objects.get_or_create(
        pk=1,
        defaults={
            'status_HP': 100,
            'status_Money': 50,
            'status_Loyalty': 0,
            'status_Herbs': 0

        }
    )
    return status_obj

def event_part_2(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)
    player_status = get_player_status()
    action = request.GET.get('action')

    if action == '1':
        consequence = event_obj.consequence_1
        # Обновляем статус при выборе действия 1
        player_status.status_HP += event_obj.received_HP
        player_status.status_Money += event_obj.received_Money
        player_status.status_Loyalty += event_obj.received_Loyalty
        player_status.status_Herbs += event_obj.received_Medicinal_herbs
    elif action == '2':
        consequence = event_obj.consequence_2
        # Обновляем статус при выборе действия 2
        player_status.status_HP += event_obj.received_HP_2
        player_status.status_Money += event_obj.received_Money_2
        player_status.status_Loyalty += event_obj.received_Loyalty_2
        player_status.status_Herbs += event_obj.received_Medicinal_herbs
    else:
        return redirect('play_next', event_id=event_id)

    # Сохраняем изменения статуса
    player_status.save()

    return render(request, 'play/play.html', {
        'event': event_obj,
        'player_status': player_status,
        'consequence': consequence,
        'show_actions': False,
        'show_event_text': False  # Добавьте эту строку
    })



def random_event(request):
    """Перенаправление на случайное событие"""
    random_id = get_random_event_id()
    if random_id:
        return redirect('play_next', event_id=random_id)
    return redirect('play')


def get_consequence(request, event_id, action):
    """API для получения последствий (AJAX)"""
    try:
        event_obj = event.objects.get(id=event_id)
        if action == 1:
            consequence = event_obj.consequence_1
        else:
            consequence = event_obj.consequence_2
        return JsonResponse({
            'consequence': consequence,
            'success': True
        })
    except event.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Event not found'
        }, status=404)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import status


@csrf_exempt
def use_herbs(request):
    if request.method == 'POST':
        try:
            player_status = status.objects.get(pk=1)

            if player_status.status_Herbs <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Недостаточно трав'
                })

            # Сохраняем старые значения для сравнения
            old_hp = player_status.status_HP

            # Обновляем значения
            player_status.status_HP += 10
            player_status.status_Herbs -= 1
            player_status.save()

            return JsonResponse({
                'success': True,
                'new_hp': player_status.status_HP,
                'new_money': player_status.status_Money,
                'new_loyalty': player_status.status_Loyalty,
                'new_herbs': player_status.status_Herbs,
                'hp_diff': player_status.status_HP - old_hp  # Разница HP для анимации
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})

