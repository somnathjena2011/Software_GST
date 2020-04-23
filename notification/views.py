from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Notification
from accounts.models import User, TaxpayerProfile, OfficialProfile
from invoice.models import Invoice
from django.contrib.auth.decorators import login_required

@login_required
def notifs(request):
	usr = request.user
	notifications = Notification.objects.filter(user=usr).filter(viewed=False)
	return render(request, 'notification/notification.html',{'notifications':notifications,'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})

@login_required
def show(request, notification_id):
	n = Notification.objects.get(id=notification_id)
	return render(request,'notification/notify.html', {'notification':n})

@login_required
def delete(request, notification_id):
	n = Notification.objects.get(id=notification_id)
	n.viewed = True
	n.save()
	return render(request, 'accounts/taxpayer_home.html', {'invoices':Invoice.objects.all(),'tax':TaxpayerProfile.objects.all(),'notifs':Notification.objects.filter(user=request.user).filter(viewed=False)})