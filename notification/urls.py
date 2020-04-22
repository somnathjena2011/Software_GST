from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'notification'

urlpatterns=[
	path('show/',views.notifs,name='notifs'),
	path('show/<int:notification_id>/',views.show,name='show'),
	path('delete/<int:notification_id>/',views.delete,name='delete'),
]