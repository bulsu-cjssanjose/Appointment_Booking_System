from django.contrib import admin
from .models import Service, Client, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'active')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'scheduled_at', 'status', 'is_archived')
    list_filter = ('status', 'is_archived')
    search_fields = ('client__full_name',)