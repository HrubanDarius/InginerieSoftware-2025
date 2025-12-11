from django.urls import path
from YoutubeToText import views

urlpatterns = [
    path("", views.temp_here, name="temp_here"),             # /yt/
    path("discover/", views.temp_somewhere, name="temp_somewhere"), # /yt/discover/
    path("dashboard/", views.view_dashboard, name="dashboard"),
path("save/", views.save_from_file, name="save_from_file"),
]