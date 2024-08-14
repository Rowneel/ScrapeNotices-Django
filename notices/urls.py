from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('update-notices/', views.update_notices, name='update_notices'),
]