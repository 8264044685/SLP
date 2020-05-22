from django.contrib import admin
from django.urls import path
from .apis import MakeModels

urlpatterns = [
    path('add-models', MakeModels.as_view()),
]