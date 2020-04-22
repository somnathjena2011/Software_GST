from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
	path('',views.payment_home,name='home'),
	path('card',views.card,name='card'),
	path('netbanking',views.netbanking,name='netbanking'),
    #path('process',views.payment_process,name='process'),
    #path('done',views.payment_done,name='done'),
    ]