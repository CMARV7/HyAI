"""
All database models for HyAI – Complete and Final
Everything you asked for is here:
- BP readings with AI advice
- Medication reminders
- User profile (age, emergency contact)
- Emergency contact system
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Extend User with extra info
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True, help_text="Your age (for better AI advice)")
    emergency_contact_name = models.CharField(max_length=100, blank=True, help_text="Name of person to contact in emergency")
    emergency_contact_email = models.EmailField(blank=True, help_text="Email to alert in crisis")
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Blood Pressure Log + AI Advice
class BloodPressureLog(models.Model):
    RISK_CHOICES = [
        ('normal', 'Normal'),
        ('elevated', 'Elevated'),
        ('high', 'High (Stage 1/2)'),
        ('crisis', 'Hypertensive Crisis'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bp_logs')
    systolic = models.PositiveIntegerField(help_text="Top number (e.g. 120)")
    diastolic = models.PositiveIntegerField(help_text="Bottom number (e.g. 80)")
    symptoms = models.TextField(blank=True, help_text="How you feel: headache, dizziness, etc.")
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='normal')
    ai_advice = models.TextField(blank=True, help_text="Real advice from AWS Bedrock AI")
    logged_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.systolic}/{self.diastolic} - {self.risk_level}"


# Medication Reminder
class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once daily'),
        ('twice', 'Twice daily'),
        ('thrice', 'Three times daily'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning (8:00 AM)'),
        ('afternoon', 'Afternoon (2:00 PM)'),
        ('evening', 'Evening (8:00 PM)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='once')
    times = models.ManyToManyField('TimeSlot', blank=True)  # Custom times
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"


class TimeSlot(models.Model):
    time = models.CharField(max_length=20, choices=Medication.TIME_CHOICES)
    label = models.CharField(max_length=30)

    def __str__(self):
        return self.label


# Health Tip (we can add more later)
class HealthTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    youtube_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
    
class MedicationTime(models.Model):
    medication = models.ForeignKey(
        Medication, 
        on_delete=models.CASCADE, 
        related_name='dose_times'  # ← CHANGED THIS LINE
    )
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime("%I:%M %p")