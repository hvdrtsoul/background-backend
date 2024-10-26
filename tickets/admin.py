from django.contrib import admin
from tickets.models import Hall, Event, EventSectorPrice, Sector

# Register your models here.

admin.site.register(Hall)
admin.site.register(Event)
admin.site.register(Sector)
admin.site.register(EventSectorPrice)