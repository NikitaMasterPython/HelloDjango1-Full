from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from dateutil.relativedelta import relativedelta  # для работы с месяцами
import django.core.validators
import random

SUMMER_BACKGROUNDS = [
    'village_summer1.png',
    'village_summer2.png',
    'village_summer3.png',
]

WINTER_BACKGROUNDS = [
    'village_winter1.png',
    'village_winter2.png',
    'village_winter3.png',
]

def validate_max_hp_100(status_HP):
    if status_HP > 100:
        raise ValidationError("Значение здоровья не может превышать 100")

def validate_max_Loyalty_100(status_Loyalty):
    if status_Loyalty > 100:
        raise ValidationError("Значение Лояльности не может превышать 100")

class status(models.Model):
    status_HP = models.IntegerField(
        default=100,
        # validators=[validate_max_hp_100],  # Добавленный валидатор
        validators=[django.core.validators.MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='game_status',
        primary_key=True  # Делаем user primary key
    )


    def save(self, *args, **kwargs):
        # Проверка и коррекция здоровья
        if self.status_HP is not None and self.status_HP > 100:
            self.status_HP = 100

        # Проверка и коррекция лояльности
        if self.status_Loyalty is not None and self.status_Loyalty > 100:
            self.status_Loyalty = 100

        super().save(*args, **kwargs)

    status_Money = models.IntegerField(default=50, null=True, blank=True)

    status_Loyalty = models.IntegerField(
        default=0,
        # validators=[validate_max_Loyalty_100],  # Добавленный валидатор
        validators=[django.core.validators.MaxValueValidator(100)],
        null=True,
        blank=True
    )

    status_Herbs = models.IntegerField(default=0)
    status_Samogon = models.IntegerField(default=0)
    status_Poison = models.IntegerField(default=0)
    status_Fish = models.IntegerField(default=0)
    status_Jewelry = models.IntegerField(default=0)
    status_Harvest = models.IntegerField(default=0)

    def reset(self):
        """Сбрасывает все параметры к значениям по умолчанию"""
        self.status_HP = 100
        self.status_Money = 10
        self.status_Loyalty = 10
        self.status_Herbs = 0
        self.status_Poison = 0
        self.status_Samogon = 0
        self.status_Fish = 0
        self.status_Jewelry = 0
        self.status_Harvest = 0
        self.save()
        return self

    @classmethod
    def get_default_status(cls, user):
        """Получает или создает статус для текущего пользователя"""
        obj, created = cls.objects.get_or_create(user=user)
        if created:
            obj.reset()
        return obj

    class Meta:
        verbose_name_plural = "statuses"

    def __str__(self):
        return f"HP: {self.status_HP}, Money: {self.status_Money}, Loyalty: {self.status_Loyalty}"

class event(models.Model):
    event_Season = models.CharField(default = "summer", max_length=500, verbose_name='Время года')
    event_Text = models.CharField(max_length=500, verbose_name = 'Текст события')
    action_1 = models.CharField(max_length=500, verbose_name = 'Действие 1')
    consequence_1 = models.CharField(max_length=500, verbose_name = 'Последствие 1')
    received_HP = models.IntegerField(default = 0, verbose_name = 'Изменение здоровья 1')
    received_Money = models.IntegerField(default = 0, verbose_name = 'Изменение монет 1')
    received_Loyalty = models.IntegerField(default = 0, verbose_name = 'Изменение лояльности 1')

    image_Event = models.ImageField(null=True, blank=True,upload_to='image/event', max_length=10000, verbose_name = 'Изображение события')

    received_Medicinal_herbs = models.IntegerField(default = 0, verbose_name = 'Лечебные травы')
    received_Samogon = models.IntegerField(default=0, verbose_name='Самогон')
    received_Poison = models.IntegerField(default=0, verbose_name='Яд')
    received_Fish = models.IntegerField(default=0, verbose_name='Рыба')
    received_Jewelry = models.IntegerField(default=0, verbose_name='Драгоценности')
    received_Harvest = models.IntegerField(default=0, verbose_name='Урожай')

    action_2 = models.CharField(max_length=500, verbose_name = 'Действие 2')
    consequence_2 = models.CharField(max_length=500, verbose_name = 'Последствие 2')
    received_HP_2 = models.IntegerField(default = 0, verbose_name = 'Изменение здоровье 2')
    received_Money_2 = models.IntegerField(default = 0, verbose_name = 'Изменение монет 2')
    received_Loyalty_2 = models.IntegerField(default = 0, verbose_name = 'Изменение лояльности 2')

    received_Medicinal_herbs_2 = models.IntegerField(default = 0, verbose_name = 'Лечебные травы')
    received_Samogon_2 = models.IntegerField(default=0, verbose_name='Самогон')
    received_Poison_2 = models.IntegerField(default=0, verbose_name='Яд')
    received_Fish_2 = models.IntegerField(default=0, verbose_name='Рыба')
    received_Jewelry_2 = models.IntegerField(default=0, verbose_name='Драгоценности')
    received_Harvest_2 = models.IntegerField(default=0, verbose_name='Урожай')

    def __str__(self):
        return self.event_Text  # Это будет отображаться в админке вместо "event object (1)"

class UserDate(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='play_game_date',
        primary_key = True
    )

    current_date = models.DateField(default=date(1600, 4, 1))
    last_event_id = models.PositiveIntegerField(null=True, blank=True)
    death_date = models.DateField(default=date(1650, 4, 1))



    current_season = models.CharField(max_length=20, blank=True)
    current_background = models.CharField(max_length=100, blank=True)


    def update_background(self, season):
        """Обновляет фон при смене сезона"""
        if season != self.current_season:
            self.current_season = season
            if season == 'winter_time':
                self.current_background = random.choice(WINTER_BACKGROUNDS)
            else:
                self.current_background = random.choice(SUMMER_BACKGROUNDS)


    def next_month(self):
        """Переход на следующий месяц"""
        old_date = self.current_date

        old_season = self.get_season()
        self.current_date += relativedelta(months=1)
        new_season = self.get_season()
        print(f"BEFORE: Current date: {old_date}, Death date: {self.death_date}")
        print(f"AFTER: Current date: {self.current_date}, Death date: {self.death_date}")


        # Обновляем фон при смене сезона
        if old_season != new_season:
            self.update_background(new_season)

        self.save()


    def reset_date(self):
        """Сброс даты к начальной"""
        self.current_date = date(1600, 4, 1)
        self.death = date(1650, 4, 1)
        self.update_background('summer_time')
        self.save()


    def get_season(self):
        """Определение текущего сезона"""
        month = self.current_date.month
        if month in [10, 11, 12, 1, 2, 3]:
            return 'winter_time'
        return 'summer_time'

    def __str__(self):
        return f"{self.user.username} - {self.current_date}"




