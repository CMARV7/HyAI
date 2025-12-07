# test_reminder.py — RUN THIS TO TEST EMAIL REMINDER
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hyai_project.settings')
django.setup()

from django.core.mail import send_mail
from django.contrib.auth.models import User

# Get first user (or replace with your username)
user = User.objects.first()

send_mail(
    'Test Medication Reminder from HyAI',
    'This is a test reminder — your medicine time is now! 💊 Stay healthy!',
    'chinwendumarvelous7@gmail.com',
    [user.email],
    fail_silently=False,
)

print("Test email sent! Check your inbox.")