from django.shortcuts import redirect
from .models import status  # Импортируем вашу модель


def play_restart(request):
    # Получаем или создаём запись статуса (если её нет)
    game_status, created = status.objects.get_or_create(pk=1)

    # Сбрасываем параметры к значениям по умолчанию
    game_status.status_HP = 100
    game_status.status_Money = 50
    game_status.status_Loyalty = 0
    game_status.status_Herbs = 0

    # Сохраняем изменения
    game_status.save()

    # Перенаправляем пользователя на страницу игры
    return redirect('play_restart/')  # Замените 'play' на имя вашего URL для игры