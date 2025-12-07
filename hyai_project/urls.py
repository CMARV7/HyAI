"""
Main URL configuration for HyAI project
All URLs go through this file
Clean, simple, perfect
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Allauth login/signup/logout
    path('accounts/', include('allauth.urls')),
    
    # Our core app – all main pages
    path('', include('core.urls')),
    
    # Fallback for any unknown URL (optional – nice 404 later)
    # path('', TemplateView.as_view(template_name='home.html'), name='root'),
]

# Custom login/logout redirects (already set in settings, but safe here too)
from django.contrib.auth import views as auth_views