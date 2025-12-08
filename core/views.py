from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
import boto3
import json
import os
from .models import BloodPressureLog, UserProfile, Medication, MedicationTime, HealthTip

@login_required
def home(request):
    return render(request, 'home.html', {'user_name': request.user.get_full_name() or request.user.username})

@login_required
def check_bp(request):
    result = None
    if request.method == "POST":
        try:
            systolic = int(request.POST['systolic'])
            diastolic = int(request.POST['diastolic'])
            symptoms = request.POST.get('symptoms', '')

            if not (40 <= systolic <= 250 and 20 <= diastolic <= 150):
                messages.error(request, "Please enter realistic BP values")
                return render(request, 'bp_check.html')

            if systolic >= 180 or diastolic >= 120:
                risk = "CRISIS"
            elif systolic <= 90 or diastolic <= 60:
                risk = "DANGER_LOW"
            elif systolic >= 140 or diastolic >= 90:
                risk = "HIGH"
            elif systolic <= 100 or diastolic <= 70:
                risk = "LOW"
            elif systolic >= 130 or diastolic >= 80:
                risk = "ELEVATED"
            else:
                risk = "NORMAL"

            try:
                client = boto3.client(
                    'bedrock-runtime',
                    region_name='us-east-1',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
                prompt = f"""You are Dr. HyAI — a professional cardiologist.
BP: {systolic}/{diastolic}, Risk: {risk.replace('_', ' ')}
Give a short, clear, structured report in 3 parts:
1. Reading & classification
2. Immediate action
3. Lifestyle tips (3-4 bullets)
Use professional English."""
                response = client.invoke_model(
                    modelId="anthropic.claude-3-haiku-20240307-v1:0",
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 350,
                        "temperature": 0.3,
                        "messages": [{"role": "user", "content": prompt}]
                    }).encode()
                )
                advice = json.loads(response['body'].read())['content'][0]['text']
            except:
                advice = "Your reading has been saved."

            BloodPressureLog.objects.create(
                user=request.user,
                systolic=systolic,
                diastolic=diastolic,
                symptoms=symptoms,
                risk_level=risk,
                ai_advice=advice
            )

            result = {'systolic': systolic, 'diastolic': diastolic, 'symptoms': symptoms, 'risk': risk, 'advice': advice}

        except ValueError:
            messages.error(request, "Please enter valid numbers")
        except Exception:
            messages.error(request, "Something went wrong")

    return render(request, 'bp_check.html', {'result': result})

@login_required
def health_records(request):
    logs = request.user.bp_logs.all().order_by('-logged_at')
    return render(request, 'health_records.html', {'logs': logs})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.age = request.POST.get('age') or None
        profile.emergency_contact_name = request.POST.get('emergency_name', '')
        profile.emergency_contact_phone = request.POST.get('emergency_phone', '')
        profile.emergency_contact_email = request.POST.get('emergency_email', '')
        profile.save()
        messages.success(request, "Profile saved!")
        return redirect('profile')
    return render(request, 'profile_edit.html', {'profile': profile})

@login_required
def medication(request):
    active_med = request.user.medications.filter(active=True).first()
    if request.method == "POST":
        if 'cancel_med' in request.POST:
            med = Medication.objects.get(id=request.POST['cancel_med'], user=request.user)
            med.active = False
            med.save()
            return redirect('medication')

        name = request.POST['name']
        med = Medication.objects.create(
            user=request.user,
            name=name,
            dosage=request.POST.get('dosage', ''),
            frequency=request.POST['frequency'],
            start_date=request.POST['start_date'],
            end_date=request.POST.get('end_date') or None,
            notes=request.POST.get('notes', '')
        )
        # ... time creation code ...
        request.user.medications.exclude(id=med.id).update(active=False)
        messages.success(request, f"{name} activated!")
        return redirect('medication')

    return render(request, 'medication.html', {
        'active_med': active_med,
        'frequency_choices': Medication.FREQUENCY_CHOICES
    })

@login_required
def health_tips(request):
    tips = HealthTip.objects.all()
    daily_tip = tips.order_by('?').first()
    return render(request, 'health_tips.html', {'tips': tips, 'daily_tip': daily_tip})

@login_required
def chat_doctor(request):
    if request.method == "POST":
        user_message = request.POST.get('message', '').strip()
        try:
            client = boto3.client(
                'bedrock-runtime',
                region_name='us-east-1',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            prompt = f"Patient says: {user_message}\nReply as Dr. HyAI — professional, caring doctor."
            response = client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "temperature": 0.8,
                    "messages": [{"role": "user", "content": prompt}]
                }).encode()
            )
            reply = json.loads(response['body'].read())['content'][0]['text']
        except:
            reply = "I'm here for you. How can I help?"
        return JsonResponse({'reply': reply})
    return render(request, 'chat_doctor.html')
