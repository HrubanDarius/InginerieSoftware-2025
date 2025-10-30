from django.urls import path

from YoutubeToText import views

urlpatterns = [
    path("YoutubeToText/",views.temp_here, name="temp_here"),
    path("YoutubeToText/discover", views.temp_somewhere, name="temp_somewhere"),

]