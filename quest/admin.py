from django.contrib import admin
from .models import Scene, Choice, GameState

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fk_name = 'scene'

@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_initial']
    list_editable = ['is_initial']
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'scene', 'next_scene']

@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_scene']
    list_filter = ['user']