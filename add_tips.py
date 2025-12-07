# add_tips.py — RUN ONCE TO ADD 5 TIPS
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hyai_project.settings')
django.setup()

from core.models import HealthTip

tips = [
    {
        "title": "How to Lower Blood Pressure Naturally",
        "content": "Simple lifestyle changes like reducing salt, exercising daily, and managing stress can significantly lower blood pressure without medication.",
        "youtube_link": "https://www.youtube.com/watch?v=6d7b0dL6J6I"
    },
    {
        "title": "Top 10 Foods That Lower Blood Pressure",
        "content": "Include bananas, spinach, berries, oatmeal, and garlic in your diet to naturally control hypertension.",
        "youtube_link": "https://www.youtube.com/watch?v=3p8EBPVZ2Iw"
    },
    {
        "title": "Prevent Heart Disease - 7 Proven Steps",
        "content": "Quit smoking, eat heart-healthy foods, exercise 30 mins daily, control cholesterol and blood pressure.",
        "youtube_link": "https://www.youtube.com/watch?v=Fu1u11iRKAE"
    },
    {
        "title": "Hypertension Prevention & Management",
        "content": "Learn from Mayo Clinic experts how to prevent and manage high blood pressure effectively.",
        "youtube_link": "https://www.youtube.com/watch?v=OmKVteeuQj0"
    },
    {
        "title": "Sudden Cardiac Arrest - Know the Signs",
        "content": "Early recognition and CPR can save lives. Learn warning signs and prevention strategies.",
        "youtube_link": "https://www.youtube.com/watch?v=5l6x8y3y3yM"
    }
]

for tip in tips:
    HealthTip.objects.create(**tip)

print("5 Health Tips Added Successfully!")