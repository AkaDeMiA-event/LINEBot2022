from django.contrib import admin
from .models import Numeron

# Register your models here.

admin.site.register(Numeron, admin.ModelAdmin)
