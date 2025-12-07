# HyAI — Your Personal Heart Guardian ❤️

**The world's first AI-powered hypertension companion**  
Real-time BP analysis • AI Doctor chat • Medication reminders • Health tips

Live Demo: https://hyai.up.railway.app (coming in 2 minutes)

## Features
- Instant BP analysis with professional AI doctor advice
- Dangerously low & high BP detection with red blinking alerts
- 24/7 Chat with Dr. HyAI (powered by AWS Claude 3)
- Daily medication reminders via email
- Personal health records & emergency profile
- Beautiful, mobile-friendly design

## Tech Stack
- Django 5.2
- AWS Bedrock (Claude 3 Haiku) — AI Doctor
- AWS SES — Email reminders
- Tailwind CSS — Premium UI
- Celery + Redis — Timed reminders
- Hosted on Railway (free forever)

## Quick Start (Local)
```bash
git clone https://github.com/CMARV7/HyAI.git
cd HyAI
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
