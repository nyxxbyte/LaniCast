from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.weather_view, name='weather'),
    # PWA configuration routes
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw'),
]