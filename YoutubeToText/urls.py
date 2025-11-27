from django.urls import path
from YoutubeToText import views

urlpatterns = [
    path("", views.temp_here, name="temp_here"),             # /yt/
    path("discover/", views.temp_somewhere, name="temp_somewhere") # /yt/discover/
]