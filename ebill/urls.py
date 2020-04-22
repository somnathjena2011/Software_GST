from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'ebill'

urlpatterns = [
    path('registration',views.ebill_view,name='ebill_form'),
    path('generated',views.generate_view,name='generated_bill'),
]