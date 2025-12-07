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

            # RISK LOGIC
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

            # AI DOCTOR — KEYS FROM ENVIRONMENT (SAFE)
            try:
                client = boto3.client(
                    'bedrock-runtime',
                    region_name='us-east-1',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
                prompt = f"""You are Dr. HyAI — a highly professional, board-certified cardiologist.
Patient BP: {systolic}/{diastolic} mmHg
Symptoms: {symptoms or 'None reported'}
Risk level: {risk.replace('_', ' ').title()}

note your response must be short and very clear it should not exceed five sentences.
Give a short, clear, structured medical report in 3 parts:
1. Current reading and classification
2. Immediate action (if crisis/danger low: GO TO HOSPITAL IMMEDIATELY)
3. Lifestyle recommendations (3-4 bullet points)

Use clean, professional English. Be caring, friendly but authoritative.
Reply now:"""

                response = client.invoke_model(
                    modelId="anthropic.claude-3-haiku-20240307-v1:0",
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 350,
                        "temperature": 0.3,
                        "messages": [{"role": "user", "content": prompt}]
                    }).encode()
                )
                result_json = json.loads(response['body'].read())
                advice = result_json['content'][0]['text']
            except Exception as e:
                advice = "Your reading has been saved. Please consult a doctor for accurate advice."

            BloodPressureLog.objects.create(
                user=request.user,
                systolic=systolic,
                diastolic=diastolic,
                symptoms=symptoms,
                risk_level=risk,
                ai_advice=advice
            )

            result = {
                'systolic': systolic,
                'diastolic': diastolic,
                'symptoms': symptoms,
                'risk': risk,
                'advice': advice
            }

        except ValueError:
            messages.error(request, "Please enter valid numbers")
        except Exception:
            messages.error(request, "Something went wrong")

    return render(request, 'bp_check.html', {'result': result})

# — ALL OTHER VIEWS SAME AS BEFORE (no keys) —
# (health_records, profile, medication, health_tips, chat_doctor — unchanged except chat_doctor below)

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
            
            prompt = f"""You are Dr. HyAI, a friendly, confident, caring professional doctor.
Always reply in short, warm, engaging sentences.
Use simple English. Add light Naija vibe only if patient uses pidgin.
Be direct, caring, and accurate.
You can suggest general medication types if needed.
Always recommend seeing a real doctor for serious cases.
Patient says: "{user_message}"
Reply now:"""

            response = client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "temperature": 0.8,
                    "messages": [{"role": "user", "content": prompt}]
                }).encode()
            )
            
            result = json.loads(response['body'].read())
            reply = result['content'][0]['text'].strip()
            
        except:
            reply = "Doctor Hyai is here for you, talk to me am here to help"

        return JsonResponse({'reply': reply})
    
    return render(request, 'chat_doctor.html')