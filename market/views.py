from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from play.models import status, UserDate  # Импорт модели из приложения play
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
import random

Herbs_cost = 5
Herbs_sell_price = 1

samogon_cost = 5
samogon_sell_price = 1

poison_cost = 5
poison_sell_price = 1

fish_cost = 5
fish_sell_price = 1

jewelry_cost = 15
jewelry_sell_price = 5

@login_required
def market(request):
    # Получаем статус текущего пользователя
    player_status = status.get_default_status(request.user)

    user_date = UserDate.objects.get(user=request.user)
    season = user_date.get_season()

    harvest_sell_price = random.randint(1, 2)
    harvest_cost = harvest_sell_price * 2

    request.session['harvest_cost'] = harvest_cost
    request.session['harvest_sell_price'] = harvest_sell_price

    request.session['jewelry_cost'] = jewelry_cost
    request.session['jewelry_sell_price'] = jewelry_sell_price

    request.session['fish_cost'] = fish_cost
    request.session['fish_sell_price'] = fish_sell_price

    request.session['samogon_cost'] = samogon_cost
    request.session['samogon_sell_price'] = samogon_sell_price

    request.session['poison_cost'] = poison_cost
    request.session['poison_sell_price'] = poison_sell_price

    request.session['Herbs_cost'] = Herbs_cost
    request.session['Herbs_sell_price'] = Herbs_sell_price

    # Обновляем фон при необходимости
    if not user_date.current_background:
        user_date.update_background(season)
        user_date.save()

    # Формируем URL фона
    background_image_url = f"{settings.STATIC_URL}image/fons/{user_date.current_background}"
    market_action = request.session.get('market_action', 'buy')

    return render(request, 'market/market.html', {
        'player_status': player_status,
        'background_image_url': background_image_url,  # Добавляем фон в контекст
        'market_action': market_action,  # Передаем действие в шаблон

        'harvest_cost': harvest_cost,  # Добавляем в контекст
        'harvest_sell_price': harvest_sell_price,  # Добавляем в контекст

        'jewelry_cost': jewelry_cost,  # Добавляем в контекст
        'jewelry_sell_price': jewelry_sell_price,  # Добавляем в контекст

        'fish_cost': fish_cost,  # Добавляем в контекст
        'fish_sell_price': fish_sell_price,  # Добавляем в контекст

        'samogon_cost': samogon_cost,  # Добавляем в контекст
        'samogon_sell_price': samogon_sell_price,  # Добавляем в контекст

        'poison_cost': poison_cost,  # Добавляем в контекст
        'poison_sell_price': poison_sell_price,  # Добавляем в контекст

        'Herbs_cost': Herbs_cost,  # Добавляем в контекст
        'Herbs_sell_price': Herbs_sell_price,  # Добавляем в контекст
    })

def save_market_action(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            action = data.get('action', 'sell')
            request.session['market_action'] = action
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'})

def buy_herbs(request, Herbs_cost=None):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            Herbs_cost = request.session.get('Herbs_cost', 2)
            Herbs_sell_price = request.session.get('Herbs_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < Herbs_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= Herbs_cost
                player_status.status_Herbs += 1
                player_status.save()
                messages.success(request, 'Травы успешно куплены!')
            else:
                # Логика продажи
                if player_status.status_Herbs < 1:
                    messages.error(request, 'Недостаточно трав для продажи')
                    return redirect('market:market')

                player_status.status_Money += Herbs_sell_price
                player_status.status_Herbs -= 1
                player_status.save()
                messages.success(request, 'Травы успешно проданы!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')

def buy_samogon(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            samogon_cost = request.session.get('samogon_cost', 2)
            samogon_sell_price = request.session.get('samogon_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < Herbs_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= samogon_cost
                player_status.status_Samogon += 1
                player_status.save()
                messages.success(request, 'Самагон успешно куплен!')
            else:
                # Логика продажи
                if player_status.status_Samogon < 1:
                    messages.error(request, 'Недостаточно самогона для продажи')
                    return redirect('market:market')

                player_status.status_Money += samogon_sell_price
                player_status.status_Samogon -= 1
                player_status.save()
                messages.success(request, 'Самогон успешно продан!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')

def buy_poison(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            poison_cost = request.session.get('poison_cost', 2)
            poison_sell_price = request.session.get('poison_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < poison_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= poison_cost
                player_status.status_Poison += 1
                player_status.save()
                messages.success(request, 'Яд успешно куплен!')
            else:
                # Логика продажи
                if player_status.status_Poison < 1:
                    messages.error(request, 'Недостаточно яда для продажи')
                    return redirect('market:market')

                player_status.status_Money += poison_sell_price
                player_status.status_Poison -= 1
                player_status.save()
                messages.success(request, 'Яд успешно продан!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')

def buy_fish(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            fish_cost = request.session.get('fish_cost', 2)
            fish_sell_price = request.session.get('fish_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < fish_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= fish_cost
                player_status.status_Fish += 1
                player_status.save()
                messages.success(request, 'Рыба успешно куплена!')
            else:
                # Логика продажи
                if player_status.status_Fish < 1:
                    messages.error(request, 'Недостаточно рыбы для продажи')
                    return redirect('market:market')

                player_status.status_Money += fish_sell_price
                player_status.status_Fish -= 1
                player_status.save()
                messages.success(request, 'Рыба успешно продана!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')

def buy_jewelry(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            jewelry_cost = request.session.get('jewelry_cost', 2)
            jewelry_sell_price = request.session.get('jewelry_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < jewelry_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= jewelry_cost
                player_status.status_Jewelry += 1
                player_status.save()
                messages.success(request, 'Драгоценности успешно куплены!')
            else:
                # Логика продажи
                if player_status.status_Jewelry < 1:
                    messages.error(request, 'Недостаточно драгоценностей для продажи')
                    return redirect('market:market')

                player_status.status_Money += jewelry_sell_price
                player_status.status_Jewelry -= 1
                player_status.save()
                messages.success(request, 'Драгоценности успешно проданы!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')

def buy_harvest(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            action_type = request.POST.get('action_type', 'buy')  # Получаем тип действия
            request.session['market_action'] = action_type
            player_status = status.objects.get(user=request.user)

            harvest_cost = request.session.get('harvest_cost', 2)
            harvest_sell_price = request.session.get('harvest_sell_price', 1)

            if action_type == 'buy':
                # Логика покупки
                if player_status.status_Money < harvest_cost:
                    messages.error(request, 'Недостаточно монет')
                    return redirect('market:market')

                player_status.status_Money -= harvest_cost
                player_status.status_Harvest += 1
                player_status.save()
                messages.success(request, 'Урожай успешно куплен!')
            else:
                # Логика продажи
                if player_status.status_Harvest < 1:
                    messages.error(request, 'Недостаточно урожая для продажи')
                    return redirect('market:market')

                player_status.status_Money += harvest_sell_price
                player_status.status_Harvest -= 1
                player_status.save()
                messages.success(request, 'Урожай успешно продан!')

            return redirect('market:market')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('market:market')
    return redirect('market:market')


