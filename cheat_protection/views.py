# cheat_protection/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from quest.models import GameState

@login_required
def cheat_warning(request):
    return render(request, 'cheat_protection/cheat_warning.html')

@login_required
def return_to_game(request):
    # Возвращаем к последней валидной сцене
    last_valid_scene = request.session.get('last_valid_scene')

    if last_valid_scene:
        # Обновляем current_scene_id чтобы избежать повторной блокировки
        request.session['current_scene_id'] = last_valid_scene
        return redirect('quest:scene', scene_id=last_valid_scene)
    else:
        # Если нет истории, возвращаем к текущей сцене из GameState
        try:
            game_state = GameState.objects.get(user=request.user)
            if game_state.current_scene:
                request.session['current_scene_id'] = game_state.current_scene.id
                return redirect('quest:scene', scene_id=game_state.current_scene.id)
        except GameState.DoesNotExist:
            pass

        # Если все остальное fails, возвращаем в главное меню квеста
        return redirect('quest:game')