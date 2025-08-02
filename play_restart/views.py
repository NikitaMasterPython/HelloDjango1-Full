from django.shortcuts import redirect

# from .models import status
# from .models import UserDate
from play.models import status, UserDate


# def play_restart(request):

    # user_date, created = UserDate.objects.get_or_create(user=request.user)
    # user_date.reset_date()
    #
    # """Полностью сбрасывает игру"""
    # # Получаем или создаем статус
    # player_status = status.get_default_status()
    #
    # # Принудительно сбрасываем параметры
    # player_status.reset()


    # Перенаправляем на страницу игры с параметром сброса
    # return redirect(f'/play?reset=true')
def play_restart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Сбрасываем статус пользователя
    player_status = status.get_default_status(request.user)
    player_status.reset()

    # Сбрасываем дату
    user_date, created = UserDate.objects.get_or_create(user=request.user)
    user_date.reset_date()

    return redirect(f'/play?reset=true')
