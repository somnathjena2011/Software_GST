from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'invoice'

urlpatterns = [
	path('upload',views.upload,name='upload'),
	path('download',views.download,name='download'),
	path('download/update',views.update,name='update'),
]