from django.contrib import admin

from .models import Customer, Deal, Gem

admin.site.register(Gem)
admin.site.register(Customer)
admin.site.register(Deal)
