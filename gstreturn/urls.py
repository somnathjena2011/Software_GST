from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'gstreturn'

urlpatterns = [
	path('',views.upload,name='home'),
	path('form',views.create_view,name='create'),
	path('return',views.gstr1_view,name='return'),
	path('return2',views.gstr2_view,name='return2'),
]