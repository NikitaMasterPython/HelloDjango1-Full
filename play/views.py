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
        'consequence': None
    })


def event_part_2(request, event_id):
    """Обработка выбора действия"""
    event_obj = get_object_or_404(event, id=event_id)
    action = request.GET.get('action')
    # player_status, _ = status.objects.get_or_create(pk=1)

    if action == '1':
        consequence = event_obj.consequence_1
        # player_status.status_HP += event_obj.received_HP
        # player_status.status_Money += event_obj.received_Money
        # player_status.status_Loyalty += event_obj.received_Loyalty
    elif action == '2':
        consequence = event_obj.consequence_2
        # player_status.status_HP += event_obj.received_HP_2
        # player_status.status_Money += event_obj.received_Money_2
        # player_status.status_Loyalty += event_obj.received_Loyalty_2
    else:
        return redirect('play_next', event_id=event_id)

    # player_status.save()

    return render(request, 'play/play.html', {
        'event': event_obj,
        'consequence': consequence,
        # 'player_status': player_status
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


