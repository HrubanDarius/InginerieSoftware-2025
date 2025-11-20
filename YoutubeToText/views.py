import datetime

import geocoder
import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse  # pt functia sa fie view
from django.shortcuts import render, redirect
from django.template import loader
from geocoder import location
from YoutubeToText.models import Worldcities


# Create your views here.
def view_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/YoutubeToText/')  # Schimbat din '/app/'
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
def temp_somewhere(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    city = random_item.city
    location = [random_item.lat, random_item.lng]
    temp = get_temp(location)

    template = loader.get_template('index.html')
    context = {
        'city' : city,
        'temp' : temp
    }


    return HttpResponse(template.render(context, request))

def temp_here(request):  #ca sa fie un view trebe sa aiba un http request ca parametru si sa returneze un http obiect
    location = geocoder.ip('me').latlng

    temp = get_temp(location)

    # template sa arate mai bn
    template = loader.get_template('index.html')
    context = {
        'city' : 'Your location',
        'temp' : temp
    }


    return HttpResponse(template.render(context, request))


def get_temp(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    return temp
