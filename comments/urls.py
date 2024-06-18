from django.contrib import admin
from django.urls import path
from comments.views import CommentListView, CommentFormView

app_name = 'comments'

urlpatterns = [
    path('', CommentListView.as_view(), name='all'),
    path('add/', CommentFormView.as_view(), name='add'),
]