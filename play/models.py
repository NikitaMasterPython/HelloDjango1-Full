from django.db import models

class status(models.Model):
    status_HP =  models.IntegerField(null=True, blank=True)
    status_Money = models.IntegerField(null=True, blank=True)
    status_Loyalty = models.IntegerField(null=True, blank=True)

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

    action_2 = models.CharField(max_length=500, verbose_name = 'Действие 2')
    consequence_2 = models.CharField(max_length=500, verbose_name = 'Последствие 2')
    received_HP_2 = models.IntegerField(default = 0, verbose_name = 'Изменение здоровье 2')
    received_Money_2 = models.IntegerField(default = 0, verbose_name = 'Изменение монет 2')
    received_Loyalty_2 = models.IntegerField(default = 0, verbose_name = 'Изменение лояльности 2')





