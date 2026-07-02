from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'address')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('name', 'email')
    list_display_links = ('id', 'name')

