from django.contrib import admin


from .models import status
admin.site.register(status)

from .models import event
admin.site.register(event)