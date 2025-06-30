from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('find_bicycles/', views.find_bicycles, name='find_bicycles'),
    path('rent_bicycle/<int:bicycle_id>/', views.rent_bicycle, name='rent_bicycle'),  # 传递自行车ID
    path('return_bicycle/<int:record_id>/', views.return_bicycle, name='return_bicycle'),  # 传递租借记录ID
    path('add_maintenance/', views.add_maintenance, name='add_maintenance'),
    path('popular_stations/', views.popular_stations, name='popular_stations'),
    path('accounts/login/', views.user_login, name='login'),  # 自定义登录视图
    path('accounts/logout/', views.user_logout, name='logout'),  # 自定义登出视图
    path('accounts/', include('django.contrib.auth.urls')),  # 包含Django自带的认证URL
]