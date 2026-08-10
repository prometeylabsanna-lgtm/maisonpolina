from django.urls import path

from src.reviews import views

app_name = "reviews"

urlpatterns = [
    path("submit/", views.review_submit, name="submit"),
]
