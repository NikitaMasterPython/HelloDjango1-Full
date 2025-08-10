from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from play.models import status, UserDate  # Импорт модели из приложения play
from django.conf import settings


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





@login_required
def mybag(request):
    # Получаем статус текущего пользователя
    player_status = status.get_default_status(request.user)

    user_date = UserDate.objects.get(user=request.user)
    season = user_date.get_season()

    # Обновляем фон при необходимости
    if not user_date.current_background:
        user_date.update_background(season)
        user_date.save()

    # Формируем URL фона
    background_image_url = f"{settings.STATIC_URL}image/fons/{user_date.current_background}"

    return render(request, 'mybag/bag.html', {
        'player_status': player_status,
        'background_image_url': background_image_url  # Добавляем фон в контекст
    })

def map_0(request):
    # Получаем статус текущего пользователя
    player_status = status.get_default_status(request.user)
    user_date = UserDate.objects.get(user=request.user)
    season = user_date.get_season()

    # Обновляем фон при необходимости
    if not user_date.current_background:
        user_date.update_background(season)
        user_date.save()

    # Формируем URL фона
    background_image_url = f"{settings.STATIC_URL}image/fons/{user_date.current_background}"

    return render(request, 'map/map_0.html', {
        'player_status': player_status,
        'background_image_url': background_image_url  # Добавляем фон в контекст
    })


def any_view(request):
    user_date = UserDate.objects.get(user=request.user)
    season = user_date.get_season()

    if not user_date.current_background:
        user_date.update_background(season)
        user_date.save()

    background_image_url = f"{settings.STATIC_URL}image/fons/{user_date.current_background}"

    return render(request, 'template.html', {
        # ... другие переменные ...
        'background_image_url': background_image_url
    })