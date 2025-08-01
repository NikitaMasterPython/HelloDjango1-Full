from django.shortcuts import render, redirect
from play.models import status  # Импорт модели из приложения play


def check_death(request):
    """Проверяет, умер ли персонаж, и перенаправляет на смерть"""
    player_status = status.get_default_status()  # Получаем статус

    if player_status.status_HP <= 0:
        return render(request, 'death/death.html', status=200)
    else:
        return redirect('play')  # Иначе возвращаем в игру

