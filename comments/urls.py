from django.contrib import admin
from django.urls import path
from comments.views import post_detail

app_name = 'comments'

urlpatterns = [
    path('', post_detail, name='all'),
]