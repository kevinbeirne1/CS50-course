from django.contrib import admin

from .models import Airport, Flight, Passenger


class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")


admin.site.register(Flight, FlightAdmin)
admin.site.register(Airport)
admin.site.register(Passenger)
# Register your models here.
