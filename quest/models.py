from django.db import models
from django.contrib.auth.models import User

# Модель сцены - основная единица игры
class Scene(models.Model):
    # Название сцены (для удобства идентификации в админке)
    title = models.CharField(max_length=100)
    # Фоновая картинка для сцены (загружается в папку scenes/)
    background_image = models.ImageField(upload_to='scenes/')
    # Текст описания сцены, который видит игрок
    description = models.TextField()
    # Флаг, указывающий, является ли сцена начальной
    is_initial = models.BooleanField(default=False)
    # Флаги, необходимые для доступа к сцене (в формате JSON)
    required_flags = models.JSONField(default=dict, blank=True)
    # Флаги, которые устанавливаются при посещении сцены (в формате JSON)
    set_flags = models.JSONField(default=dict, blank=True)
    # Необходимые предметы
    required_items = models.JSONField(default=dict, blank=True)
    # Предметы, которые изменяются (прибавляются или уменьшаются) при посещении сцены
    received_items = models.JSONField(default=dict, blank=True)
    # Описание которое появляется при наведении на выбор, который еще закрыт (нет предмета или нужного флага)
    description_stop = models.JSONField(default=dict, blank=True)

    # Строковое представление объекта для удобства отображения
    def __str__(self):
        return self.title

# Модель варианта выбора в сцене
class Choice(models.Model):
    # Связь с родительской сценой (один ко многим)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='choices')
    # Текст варианта выбора, который видит игрок
    text = models.CharField(max_length=200)
    # Ссылка на следующую сцену при выборе этого варианта
    next_scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True)
    # Флаги, необходимые для отображения этого варианта выбора
    required_flags = models.JSONField(default=dict, blank=True)
    # Необходимые предметы
    required_items = models.JSONField(default=dict, blank=True)
    # Предметы, которые изменяются (прибавляются или уменьшаются) при выборе
    received_items_choise = models.JSONField(default=dict, blank=True)
    # Описание которое появляется при наведении на выбор, который еще закрыт (нет предмета или нужного флага)
    description_stop = models.JSONField(default=dict, blank=True)
    # существующие поля...
    next_scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True)
    # Добавьте это поле для перехода на страницу смерти
    death_redirect = models.BooleanField(default=False)

    # Строковое представление объекта
    def __str__(self):
        return f"{self.scene.title} -> {self.text}"

# Модель состояния игры для каждого пользователя
class GameState(models.Model):
    # Связь с пользователем Django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Флаги игрока (прогресс, инвентарь и т.д.)
    flags = models.JSONField(default=dict)
    # Текущая сцена, в которой находится игрок
    current_scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True)
    # Время создания записи (автоматически устанавливается при создании)
    created_at = models.DateTimeField(auto_now_add=True)
    # Время последнего обновления (автоматически обновляется при каждом сохранении)
    updated_at = models.DateTimeField(auto_now=True)

    # Строковое представление объекта
    def __str__(self):
        scene_title = self.current_scene.title if self.current_scene else "No scene"
        return f"{self.user.username} - {scene_title}"