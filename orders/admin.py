from django.contrib import admin

from orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at')
    search_fields = ('customer__name', 'status')
    list_filter = ('status', 'created_at')   
    list_display_links = ('id', 'customer')
