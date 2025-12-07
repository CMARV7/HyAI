from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check-bp/', views.check_bp, name='check_bp'),
    path('records/', views.health_records, name='health_records'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('medication/', views.medication, name='medication'),
    path('health-tips/', views.health_tips, name='health_tips'),
    path('chat-doctor/', views.chat_doctor, name='chat_doctor'),
]