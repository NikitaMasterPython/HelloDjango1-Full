from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import event
import random


# from django.http import  JsonResponse
def get_random_event_id():
    """Вспомогательная функция для получения случайного ID события"""
    event_ids = list(event.objects.values_list('id', flat=True))
    return random.choice(event_ids) if event_ids else None

def play(request):
    """Перенаправление на случайное событие"""
    random_id = get_random_event_id()
    if random_id:
        return redirect('play_next', event_id=random_id)
    return render(request, 'play/play.html')

def play_next(request, event_id):
    """Обработка события"""
    Event = get_object_or_404(event, id=event_id)
    context = {
        'event': Event,
        'random_event_id': get_random_event_id()  # Передаем случайный ID в шаблон
    }
    return render(request, 'play/play.html', context)

def event_part_2 (request, event_id):
    Event = get_object_or_404(event, id=event_id)
    return render(request,'play/play.html', {'event': Event})

def random_event(request):
    random_id = get_random_event_id()
    if random_id:
        return redirect('play_next', event_id=random_id)
    return redirect('play')


def get_consequence(request):
    event_id = request.GET.get('event_id')
    action = request.GET.get('action')

    try:
        event_obj = event.objects.get(id=event_id)
        consequence = event_obj.consequence_1 if action == '1' else event_obj.consequence_2
        return JsonResponse({
            'consequence': consequence,
            'success': True
        })
    except event.DoesNotExist:
        return JsonResponse({'success': False}, status=404)







