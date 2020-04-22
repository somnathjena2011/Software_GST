from django.contrib import admin
from .models import Invoice, Return1, Return2
# Register your models here.
admin.site.register(Invoice)
admin.site.register(Return1)
admin.site.register(Return2)