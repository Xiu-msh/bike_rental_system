from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Station, Bicycle, RentalRecord, MaintenanceRecord
from .forms import RegistrationForm, ReturnBicycleForm, MaintenanceForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import math
from django.utils import timezone


def home(request):
    popular_stations = Station.objects.annotate(
        rent_count=Count('bicycle__rentalrecord'),
        bicycle_count=Count('bicycle')
    ).order_by('-rent_count')[:5]

    rental_records = []
    if request.user.is_authenticated:
        rental_records = RentalRecord.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'popular_stations': popular_stations,
        'user': request.user,
        'rental_records': rental_records
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def find_bicycles(request):
    user_latitude = 30.00 # 需要结合其他API 此处给出固定的用户纬度
    user_longitude = 120.00  # 需要结合其他API 此处给出固定的用户经度
    stations = Station.objects.all()
    nearby_stations = []
    for station in stations:
        distance = haversine(user_latitude, user_longitude, station.latitude, station.longitude)
        # if distance <= 1:  # 此处需要进行距离判断然后筛选 当前只实验功能不做判断
        nearby_stations.append(station)
    available_bicycles = Bicycle.objects.filter(status='可用', station__in=nearby_stations)
    return render(request, 'find_bicycles.html', {'bicycles': available_bicycles})


@login_required
def rent_bicycle(request, bicycle_id):
    bicycle = get_object_or_404(Bicycle, id=bicycle_id)
    if request.method == 'POST':
        if 'agree_terms' in request.POST:
            bicycle.status = '已租'
            bicycle.save()
            record = RentalRecord(user=request.user, bicycle=bicycle)
            record.save()
            return redirect('home')
        else:
            # 用户未勾选同意条款
            return render(request, 'rent_bicycle.html',
                          {'bicycle': bicycle, 'error_message': 'You must agree to the terms and conditions.'})
    return render(request, 'rent_bicycle.html', {'bicycle': bicycle})


@login_required
def return_bicycle(request, record_id):
    record = get_object_or_404(RentalRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        record.return_time = timezone.now()
        record.save()
        bicycle = record.bicycle
        bicycle.status = '可用'
        bicycle.save()
        return redirect('home')
    return render(request, 'return_bicycle.html', {'record': record})


@login_required
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaintenanceForm()
    return render(request, 'add_maintenance.html', {'form': form})


@login_required
def popular_stations(request):
    popular_stations = Station.objects.annotate(rent_count=Count('bicycle__rentalrecord')).order_by('-rent_count')[:5]
    return render(request, 'popular_stations.html', {'stations': popular_stations})


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径（公里）
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
