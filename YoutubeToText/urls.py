from django.urls import path
from YoutubeToText import views

app_name = 'YoutubeToText'

urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert_youtube, name='convert_youtube'),
    path('dashboard/', views.view_dashboard, name='dashboard'),
    path('save/', views.save_from_file, name='save_from_file'),
    path('view/<int:video_id>/', views.view_video_detail, name='view_video_detail'),
]