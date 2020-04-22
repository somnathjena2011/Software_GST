from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
	path('',views.choose,name='choose'),
	path('taxpayer',views.taxpayer_home,name='taxpayer_home'),
	path('official',views.official_home,name='official_home'),
    path('taxpayer/registration',views.taxpayer_profile_view,name='taxpayer'),
    path('official/registration',views.official_profile_view,name='official'),
    path('taxpayer/login',views.taxpayer_login,name='taxpayer_login'),
    path('official/login',views.official_login,name='official_login'),
    path('taxpayer/logout',views.taxpayer_logout,name='taxpayer_logout'),
    path('official/logout',views.official_logout,name='official_logout'),
]