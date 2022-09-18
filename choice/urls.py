from django.urls import include, path
from . import views

app_name = "choice"

urlpatterns = [
    path("choice/", views.choice.as_view(), name="choice"),
]
