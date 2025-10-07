from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from play.models import status, UserDate
from quest.models import GameState, Scene

def play_restart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # Сбрасываем статус пользователя
        player_status = status.get_default_status(request.user)
        player_status.reset()

        # Сбрасываем дату
        user_date, created = UserDate.objects.get_or_create(user=request.user)
        user_date.reset_date()

        # Получаем начальную сцену
        try:
            initial_scene = Scene.objects.get(is_initial=True)
        except (Scene.DoesNotExist, ObjectDoesNotExist):
            initial_scene = Scene.objects.first()

        # Обрабатываем состояние игры
        try:
            game_state = GameState.objects.get(user=request.user)
            game_state.flags = {}  # Очищаем все флаги
            game_state.current_scene = initial_scene  # Устанавливаем начальную сцену
            game_state.save()
        except GameState.DoesNotExist:
            # Создаем новое состояние игры, если его нет
            if initial_scene:
                GameState.objects.create(
                    user=request.user,
                    flags={},
                    current_scene=initial_scene
                )

    except Exception as e:
        # Логирование ошибки (в реальном приложении лучше использовать logging)
        print(f"Error during restart: {e}")
        # Все равно перенаправляем пользователя

    return redirect('/play?reset=true')