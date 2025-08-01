from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import event
import random
from django.shortcuts import render, get_object_or_404, redirect
from death.views import check_death  # Импортируем проверку смерти
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import event, status  # Добавляем импорт модели status
import random

from .models import UserDate




def get_random_event_id():
    """Получение случайного ID события"""
    event_ids = list(event.objects.values_list('id', flat=True))
    return random.choice(event_ids) if event_ids else None


# def play(request):
#     """Главная страница игры"""
#     random_id = get_random_event_id()
#     if random_id:
#         return redirect('play_next', event_id=random_id)
#     return render(request, 'play/play.html')

def play(request):
    """Главная страница игры с обработкой сброса"""
    # Обработка параметра сброса
    if request.GET.get('reset') == 'true':
        player_status = status.get_default_status()
        player_status.reset()

        user_date, created = UserDate.objects.get_or_create(user=request.user)
        user_date.reset_date()
    else:
        player_status = status.get_default_status()

        user_date, created = UserDate.objects.get_or_create(user=request.user)
        user_date.reset_date()

    random_id = get_random_event_id()
    if random_id:
        return redirect('play_next', event_id=random_id)

    return render(request, 'play/play.html', {
        'player_status': player_status
    })


def play_next(request, event_id):
    """Обработка конкретного события с проверкой сброса"""
    event_obj = get_object_or_404(event, id=event_id)

    # Проверяем параметр сброса
    if request.GET.get('reset') == 'true':
        player_status = status.get_default_status()
        player_status.reset()


    else:
        player_status = status.get_default_status()



    return render(request, 'play/play.html', {
        'event': event_obj,
        'player_status': player_status,
        'consequence': None,
        'show_event_text': True
    })
# def play_next(request, event_id):
#     """Обработка конкретного события"""
#     event_obj = get_object_or_404(event, id=event_id)
#     player_status, _ = status.objects.get_or_create(pk=1)
#
#     return render(request, 'play/play.html', {
#         'event': event_obj,
#         'player_status': player_status,
#         'consequence': None,
#         'show_event_text': True
#
#     })
def get_player_status():
    """Получаем или создаем статус игрока с значениями по умолчанию"""
    status_obj, created = status.objects.get_or_create(
        pk=1,
        defaults={
            'status_HP': 100,
            'status_Money': 50,
            'status_Loyalty': 0,
            'status_Herbs': 0,
            'status_Samogon': 0,
            'status_Poison': 0,
            'status_Fish': 0,
            'status_Jewelry': 0

        }
    )
    return status_obj

def event_part_2(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)
    player_status = status.get_default_status()
    # player_status = get_player_status()
    action = request.GET.get('action')



    if action == '1':
        consequence = event_obj.consequence_1
        # Обновляем статус при выборе действия 1
        player_status.status_HP += event_obj.received_HP
        player_status.status_Money += event_obj.received_Money
        player_status.status_Loyalty += event_obj.received_Loyalty
        player_status.status_Herbs += event_obj.received_Medicinal_herbs
        player_status.status_Samogon += event_obj.received_Samogon
        player_status.status_Poison += event_obj.received_Poison
        player_status.status_Fish += event_obj.received_Fish
        player_status.status_Jewelry += event_obj.received_Jewelry

    elif action == '2':
        consequence = event_obj.consequence_2
        # Обновляем статус при выборе действия 2
        player_status.status_HP += event_obj.received_HP_2
        player_status.status_Money += event_obj.received_Money_2
        player_status.status_Loyalty += event_obj.received_Loyalty_2
        player_status.status_Samogon += event_obj.received_Samogon_2
        player_status.status_Poison += event_obj.received_Poison_2
        player_status.status_Fish += event_obj.received_Fish_2
        player_status.status_Jewelry += event_obj.received_Jewelry_2
    else:
        return redirect('play_next', event_id=event_id)

    # Сохраняем изменения статуса
    player_status.save()

    if player_status.status_HP <= 0:
        return redirect('death_page')

    return render(request, 'play/play.html', {
        'event': event_obj,
        'player_status': player_status,
        'consequence': consequence,
        'show_actions': False,
        'show_event_text': False  # Добавьте эту строку
    })


def random_event(request):
    """Перенаправление на случайное событие с обновлением даты"""
    if request.user.is_authenticated:
        user_date = UserDate.objects.get(user=request.user)
        user_date.next_month()

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


def use_Samogon(request):
    if request.method == 'POST':
        try:
            player_status = status.objects.get(pk=1)

            if player_status.status_Samogon <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Недостаточно бухла'
                })

            # Сохраняем старые значения для сравнения
            old_hp = player_status.status_HP

            # Обновляем значения
            player_status.status_HP += 5
            player_status.status_Samogon -= 1
            player_status.save()

            return JsonResponse({
                'success': True,
                'new_hp': player_status.status_HP,
                'new_money': player_status.status_Money,
                'new_loyalty': player_status.status_Loyalty,
                'new_herbs': player_status.status_Herbs,
                'new_Samogon': player_status.status_Samogon,
                'hp_diff': player_status.status_HP - old_hp  # Разница HP для анимации
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def use_Poison(request):
    if request.method == 'POST':
        try:
            player_status = status.objects.get(pk=1)

            if player_status.status_Poison <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Ты че, дурак? Это не пьют!'
                })

            # Сохраняем старые значения для сравнения
            old_hp = player_status.status_HP

            # Обновляем значения
            player_status.status_HP -= 50
            player_status.status_Poison -= 1
            player_status.save()

            return JsonResponse({
                'success': True,
                'new_hp': player_status.status_HP,
                'new_money': player_status.status_Money,
                'new_loyalty': player_status.status_Loyalty,
                'new_herbs': player_status.status_Herbs,
                'new_Samogon': player_status.status_Samogon,
                'new_Poison': player_status.status_Poison,
                'hp_diff': player_status.status_HP - old_hp  # Разница HP для анимации
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def use_Fish(request):
    if request.method == 'POST':
        try:
            player_status = status.objects.get(pk=1)

            if player_status.status_Fish <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Иди лови!'
                })

            # Сохраняем старые значения для сравнения
            old_hp = player_status.status_HP

            # Обновляем значения
            player_status.status_HP += 5
            player_status.status_Fish -= 1
            player_status.save()

            return JsonResponse({
                'success': True,
                'new_hp': player_status.status_HP,
                'new_money': player_status.status_Money,
                'new_loyalty': player_status.status_Loyalty,

                'new_Fish': player_status.status_Fish,
                'hp_diff': player_status.status_HP - old_hp  # Разница HP для анимации
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def use_Jewelry(request):
    if request.method == 'POST':
        try:
            player_status = status.objects.get(pk=1)

            if player_status.status_Jewelry >= 0:
                return JsonResponse({
                    'success': False,
                    'attention': 'Если найдешь драгоценности, их можно выгодно продать!'
                })

            # Сохраняем старые значения для сравнения
            old_hp = player_status.status_HP

            # Обновляем значения


            return JsonResponse({
                'success': True,
                'new_hp': player_status.status_HP,
                'new_money': player_status.status_Money,
                'new_loyalty': player_status.status_Loyalty,

                'new_Fish': player_status.status_Fish,
                'hp_diff': player_status.status_HP - old_hp  # Разница HP для анимации
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})




