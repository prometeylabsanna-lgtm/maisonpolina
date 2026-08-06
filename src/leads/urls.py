from django.urls import path

from src.leads import views

app_name = "leads"

urlpatterns = [
    path("form/", views.lead_form, name="form"),
    path("submit/", views.lead_submit, name="submit"),
]
