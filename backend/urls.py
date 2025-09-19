# backend/urls.py

from django.contrib import admin
from django.urls import path
from lunch import views

# 아래 urlpatterns 부분을 통째로 복사해서 붙여넣어 보세요.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/restaurants', views.find_restaurants, name='find_restaurants'),
]