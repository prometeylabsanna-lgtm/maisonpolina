from django.urls import path

from src.reviews import views

app_name = "reviews"

urlpatterns = [
    path("form/", views.review_form, name="form"),
    path("submit/", views.review_submit, name="submit"),
]
