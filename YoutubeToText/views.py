import datetime
import os

import geocoder
import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse  # pt functia sa fie view
from django.shortcuts import render, redirect
from django.template import loader
from geocoder import location

from IS2025 import settings
from YoutubeToText.models import Worldcities, ConvertedVideo


# Create your views here.
def index(request):
    converted_text = request.session.get('converted_text', '')
    return render(request, 'index.html', {'converted_text': converted_text})
def view_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('YoutubeToText:index')  # MODIFICĂ AICI
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def view_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('/')

    return render(request, 'signup.html')
def save_from_file(request):
    """Funcție dedicată pentru salvarea textului din de_citit.txt"""
    if request.method == 'POST':
        file_path = os.path.join(settings.BASE_DIR, 'de_citit.txt')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                messages.error(request, 'de_citit.txt is empty! Add YouTube text first.')
            else:
                title = request.POST.get('title',
                    'YouTube_Conversion_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

                ConvertedVideo.objects.create(
                    title=title,
                    content=content,
                    user=request.user if request.user.is_authenticated else None
                )

                messages.success(request, f'Text saved successfully as "{title}"!')

                # Golește fișierul după salvare
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')

        except FileNotFoundError:
            messages.error(request, 'de_citit.txt not found!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return redirect('YoutubeToText:index')


def view_dashboard(request):
    # Afișează conversiile salvate
    if request.user.is_authenticated:
        converted_videos = ConvertedVideo.objects.filter(user=request.user)
    else:
        converted_videos = ConvertedVideo.objects.all()

    return render(request, 'dashboard.html', {
        'converted_videos': converted_videos
    })
def view_video_detail(request, video_id):
    try:
        video = ConvertedVideo.objects.get(id=video_id)
        return render(request, 'video_detail.html', {'video': video})
    except ConvertedVideo.DoesNotExist:
        messages.error(request, 'Video not found!')
        return redirect('YoutubeToText:dashboard')
def convert_youtube(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')

        try:
            import yt_dlp
            import whisper
            import os

            # 1. Download audio
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/audio.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            # 2. Transcrie cu Whisper
            model = whisper.load_model("base")
            result = model.transcribe("downloads/audio.mp3")

            # 3. Salvează în de_citit.txt
            file_path = os.path.join(settings.BASE_DIR, 'de_citit.txt')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result['text'])

            # 4. Salvează textul în sesiune pentru afișare
            request.session['converted_text'] = result['text']

            # 5. Șterge fișierul audio temporar
            os.remove('downloads/audio.mp3')

            messages.success(request, '✅ Video converted successfully!')

        except Exception as e:
            messages.error(request, f'❌ Conversion failed: {str(e)}')

    return redirect('YoutubeToText:index')