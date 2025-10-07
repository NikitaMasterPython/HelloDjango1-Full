from django.shortcuts import render, redirect
from play.models import status, UserDate

def check_victory_money(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_date = UserDate.objects.get(user=request.user)
    except UserDate.DoesNotExist:
        return redirect('create_character')  # Перенаправление, если статуса нет

    try:
        # Получаем статус персонажа
        player_status = status.get_default_status(request.user)
    except status.DoesNotExist:  # Добавляем обработку отсутствия статуса
        return redirect('create_character')

    # Проверка условий смерти
    if player_status.status_Money >= 1000:
        return render(request, 'death/bankrot.html', status=200)

    return redirect('play')

def check_victory_loyalty(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_date = UserDate.objects.get(user=request.user)
    except UserDate.DoesNotExist:
        return redirect('create_character')  # Перенаправление, если статуса нет

    try:
        # Получаем статус персонажа
        player_status = status.get_default_status(request.user)
    except status.DoesNotExist:  # Добавляем обработку отсутствия статуса
        return redirect('create_character')

    # Проверка условий смерти
    if player_status.status_Loyalty >= 100:
        return render(request, 'death/bankrot.html', status=200)

    return redirect('play')