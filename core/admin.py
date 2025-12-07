from django.contrib import admin
from .models import BloodPressureLog, UserProfile, Medication, MedicationTime, HealthTip

@admin.register(BloodPressureLog)
class BloodPressureLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'systolic', 'diastolic', 'risk_level', 'logged_at')
    list_filter = ('risk_level', 'logged_at')
    search_fields = ('user__username',)
    readonly_fields = ('logged_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'emergency_contact_name', 'emergency_contact_phone')
    search_fields = ('user__username', 'emergency_contact_name')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dosage', 'frequency', 'start_date', 'active')
    list_filter = ('frequency', 'active')
    search_fields = ('user__username', 'name')

@admin.register(MedicationTime)
class MedicationTimeAdmin(admin.ModelAdmin):
    list_display = ('medication', 'time')
    list_filter = ('time',)

@admin.register(HealthTip)
class HealthTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'youtube_link')
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'youtube_link')