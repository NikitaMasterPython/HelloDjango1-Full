from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Scene, GameState, Choice
from play.models import status, UserDate

def check_conditions(player_flags, player_status, required_flags, required_items):
    for key, value in required_flags.items():
        if key not in player_flags or player_flags[key] != value:
            return False
    for item, required_count in required_items.items():
        current_count = getattr(player_status, f"status_{item}", 0)
        if current_count < required_count:
            return False
    return True

def apply_items_changes(player_status, items_changes):
    for item, change in items_changes.items():
        if change != 0:
            current_value = getattr(player_status, f"status_{item}", 0)
            new_value = current_value + change
            if new_value < 0:
                new_value = 0
            setattr(player_status, f"status_{item}", new_value)
    player_status.save()

def check_death_conditions(player_status):
    """Проверяет все условия смерти"""
    if player_status.status_HP <= 0:
        return 'death'
    elif player_status.status_Money <= 0:
        return 'bankrot'
    elif player_status.status_Loyalty <= 0:
        return 'loyalty'
    return None

@login_required
def game_view(request):
    try:
        initial_scene = Scene.objects.get(is_initial=True)
    except Scene.DoesNotExist:
        initial_scene = Scene.objects.first()

    game_state, created = GameState.objects.get_or_create(
        user=request.user,
        defaults={'flags': {}, 'current_scene': initial_scene}
    )

    if game_state.current_scene is None:
        if initial_scene:
            game_state.current_scene = initial_scene
            game_state.save()
        else:
            return render(request, 'quest/error.html', {
                'message': 'В игре нет доступных сцен. Обратитесь к администратору.'
            })

    # Очищаем сессию и устанавливаем начальные значения
    request.session['current_scene_id'] = game_state.current_scene.id
    request.session['last_valid_scene'] = game_state.current_scene.id

    return redirect('quest:scene', scene_id=game_state.current_scene.id)

def tupic_view(request):
    return render(request, 'quest/quest_tupic.html')

@login_required
@never_cache
def scene(request, scene_id):
    # УЛУЧШЕННАЯ ПРОВЕРКА: учитываем реферер
    referer = request.META.get('HTTP_REFERER', '')
    current_scene_id = request.session.get('current_scene_id')

    # Легальные случаи:
    # 1. Первый заход (нет current_scene_id)
    # 2. Переход из make_choice
    # 3. Обновление страницы (реферер содержит текущую сцену)
    # 4. Редирект при отсутствии предмета (реферер содержит quest:scene)
    is_legal = (
            current_scene_id is None or
            'make_choice' in referer or
            f'scene/{scene_id}' in referer or
            'quest:scene' in referer or
            request.session.get('is_redirecting', False)  # Флаг редиректа
    )

    if not is_legal and current_scene_id != scene_id:
        return redirect('cheat_protection:cheat_warning')

    # Сбрасываем флаг редиректа
    request.session['is_redirecting'] = False

    # Обновляем текущую сцену в сессии
    request.session['current_scene_id'] = scene_id
    request.session['last_valid_scene'] = scene_id

    player_status = status.get_default_status(request.user)

    death_type = check_death_conditions(player_status)
    if death_type:
        request.session.pop('current_scene_id', None)
        request.session.pop('last_valid_scene', None)
        return redirect(f'death:{death_type}')

    scene = get_object_or_404(Scene, id=scene_id)

    try:
        initial_scene = Scene.objects.get(is_initial=True)
    except Scene.DoesNotExist:
        initial_scene = Scene.objects.first()

    game_state, created = GameState.objects.get_or_create(
        user=request.user,
        defaults={'flags': {}, 'current_scene': initial_scene}
    )

    # Проверяем доступность сцены
    if not check_conditions(game_state.flags, player_status, scene.required_flags, scene.required_items):
        scene_blocked_message = scene.description_stop.get('text', 'Эта сцена пока недоступна')
        messages.error(request, scene_blocked_message)
        # Устанавливаем флаг редиректа
        request.session['is_redirecting'] = True
        return redirect('quest:scene', scene_id=game_state.current_scene.id)

    # Применяем изменения предметов
    if scene.received_items:
        apply_items_changes(player_status, scene.received_items)
        death_type = check_death_conditions(player_status)
        if death_type:
            request.session.pop('current_scene_id', None)
            request.session.pop('last_valid_scene', None)
            return redirect(f'death:{death_type}')

    game_state.flags.update(scene.set_flags)
    game_state.current_scene = scene
    game_state.save()

    available_choices = []
    blocked_choices = []

    for choice in scene.choices.all():
        if check_conditions(game_state.flags, player_status, choice.required_flags, choice.required_items):
            available_choices.append(choice)
        else:
            blocked_choices.append({
                'choice': choice,
                'description': choice.description_stop.get('text', 'Это действие пока недоступна')
            })

    response = render(request, 'quest/quest_fisher.html', {
        'scene': scene,
        'choices': available_choices,
        'blocked_choices': blocked_choices,
        'game_state': game_state,
        'player_status': player_status,
    })

    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

@login_required
def make_choice(request):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        choice = get_object_or_404(Choice, id=choice_id)
        game_state = GameState.objects.get(user=request.user)
        player_status = status.get_default_status(request.user)

        if check_conditions(game_state.flags, player_status, choice.required_flags,
                            choice.required_items):

            if choice.received_items_choise:
                apply_items_changes(player_status, choice.received_items_choise)

            if choice.text.strip().lower() == "начать заново":
                request.session.pop('current_scene_id', None)
                request.session.pop('last_valid_scene', None)
                return redirect('play_restart')

            elif choice.text.strip().lower() == "вернуться к своим делам":
                request.session.pop('current_scene_id', None)
                request.session.pop('last_valid_scene', None)
                return redirect('play')

            elif choice.next_scene:
                # Обновляем текущую сцену ДО перехода
                request.session['current_scene_id'] = choice.next_scene.id
                return redirect('quest:scene', scene_id=choice.next_scene.id)
            else:
                messages.error(request, "Нет следующей сцены для этого выбора")
        else:
            messages.error(request, "Этот выбор недоступен")

    # Если что-то пошло не так, возвращаем к текущей сцене
    game_state = GameState.objects.get(user=request.user)
    return redirect('quest:scene', scene_id=game_state.current_scene.id)