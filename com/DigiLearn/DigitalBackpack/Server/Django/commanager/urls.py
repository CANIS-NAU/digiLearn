from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="templates/index.html")),
]