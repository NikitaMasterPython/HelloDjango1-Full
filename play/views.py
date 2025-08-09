from django.shortcuts import render, get_object_or_404, redirect
from play.models import event
import random
from .models import UserDate, status
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


@never_cache
def get_player_status(request):
    # ваш существующий код
    return JsonResponse({...})

def get_random_event_id(user, exclude_id=None):
    # Получаем дату пользователя (создаем если не существует)
    user_date, created = UserDate.objects.get_or_create(user=user)

    # Определяем текущий сезон пользователя
    current_season = "winter" if user_date.get_season() == "winter_time" else "summer"

    # Получаем ID событий, соответствующих текущему сезону
    event_ids = list(
        event.objects
        .filter(event_Season=current_season)
        .values_list('id', flat=True)
    )

    # Исключаем предыдущее событие если нужно
    if exclude_id is not None and exclude_id in event_ids:
        event_ids.remove(exclude_id)

    return random.choice(event_ids) if event_ids else None




def play(request):
    """Главная страница игры с обработкой сброса"""

    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем неаутентифицированных пользователей

    player_status, created = status.objects.get_or_create(user=request.user)
    user_date, created = UserDate.objects.get_or_create(user=request.user)
    """Сброс игры Новая игра"""
    if request.GET.get('reset') == 'true':
        # Сброс состояния
        player_status.reset()
        user_date.reset_date()
        # Сбрасываем последнее событие
        user_date.last_event_id = None
        user_date.save()

        # Получаем случайное событие, исключая последнее
    random_id = get_random_event_id(request.user, user_date.last_event_id)

    # Если не нашли подходящее, берем любое
    if not random_id:
        random_id = get_random_event_id(request.user)

    # Обновляем последнее событие пользователя
    user_date.last_event_id = random_id
    user_date.save()

    return redirect('play_next', event_id=random_id)


def play_next(request, event_id):
    """Обработка конкретного события"""
    # Получаем объект события
    event_obj = get_object_or_404(event, id=event_id)

    # Получаем статус пользователя
    player_status = status.get_default_status(request.user)

    # Обновляем последнее событие в UserDate
    user_date = UserDate.objects.get(user=request.user)
    user_date.last_event_id = event_id
    user_date.save()

    return render(request, 'play/play.html', {
        'event': event_obj,
        'player_status': player_status,
        'consequence': None,
        'show_event_text': True,

        'show_actions': True  # Добавляем эту переменную
    })


@never_cache
def get_player_status(request):
    # Получаем или создаем статус для пользователя
    player_status = status.get_default_status(request.user)

    return JsonResponse({
        'hp': player_status.status_HP,
        'money': player_status.status_Money,
        'loyalty': player_status.status_Loyalty,
        'herbs': player_status.status_Herbs,
        'samogon': player_status.status_Samogon,
        'poison': player_status.status_Poison,
        'fish': player_status.status_Fish,
        'jewelry': player_status.status_Jewelry,
    })

def event_part_2(request, event_id):
    event_obj = get_object_or_404(event, id=event_id)
    player_status = status.get_default_status(request.user)
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
    """Перенаправление на случайное событие"""
    if not request.user.is_authenticated:
        return redirect('login')

    # Обновляем дату
    user_date = UserDate.objects.get(user=request.user)
    user_date.next_month()

    # Получаем случайное событие, исключая последнее
    random_id = get_random_event_id(request.user, user_date.last_event_id)

    # Если не нашли подходящее, берем любое
    if not random_id:
        random_id = get_random_event_id(request.user)

    # Обновляем последнее событие
    user_date.last_event_id = random_id
    user_date.save()

    return redirect('play_next', event_id=random_id)


    # random_id = get_random_event_id()
    # if random_id:
    #     return redirect('play_next', event_id=random_id)
    # return redirect('play')

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
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            player_status = status.objects.get(user=request.user)

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
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            player_status = status.objects.get(user=request.user)

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
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            player_status = status.objects.get(user=request.user)

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
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            player_status = status.objects.get(user=request.user)

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
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            player_status = status.objects.get(user=request.user)

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




