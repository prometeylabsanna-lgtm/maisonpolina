from django.urls import path

from src.core import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
]
