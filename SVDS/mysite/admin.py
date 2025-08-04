from django.contrib import admin

# Register your models here.

from .models import Orders

# @admin.register(Orders)
# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ['id', 'date', 'transit_from', 'transit_to', 'delivery_status', 'payment_status']
#     list_filter  = ['delivery_status', 'payment_status', 'date']
#     search_fields = ['transit_from', 'transit_to', 'consignor', 'consignee']


from django.contrib import admin
from .models import Orders

# for PDFs 

# Custom filter for Delivery Status
class DeliveryStatusFilter(admin.SimpleListFilter):
    title = 'Delivery Status'  # Display title in the admin sidebar
    parameter_name = 'delivery_status'  # URL parameter name

    def lookups(self, request, model_admin):
        # Options shown in the filter sidebar
        return Orders.STATUS_CHOICES

    def queryset(self, request, queryset):
        # Apply filtering based on selected value
        if self.value():
            return queryset.filter(delivery_status=self.value())
        return queryset

# Custom filter for Payment Status
class PaymentStatusFilter(admin.SimpleListFilter):
    title = 'Payment Status'
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return Orders.PAYMENT_STATUS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(payment_status=self.value())
        return queryset

# Admin class for Orders
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'date')
    list_display = (
        'id',
        'date',
        'vehicle_number',
        'delivery_status',
        'payment_status',
        'total_charge'
    )

    list_filter = (
        DeliveryStatusFilter,
        PaymentStatusFilter,
        'date',
    )

    search_fields = (
        'vehicle_number',
        'eway_bill',
        'invoice_number',
        'transit_from',
        'transit_to'
    )

    readonly_fields = ('total_charge',)

    # Optional: add fieldsets for better UI
    fieldsets = (
        ('Order Date', {
            'fields': ('date',)
        }),
        ('Vehicle Details', {
            'fields': ('vehicle_number', 'vehicle_charge')
        }),
        ('Transit Details', {
            'fields': ('transit_from', 'transit_to', 'consignor', 'consignee')
        }),
        ('Consignment Details', {
            'fields': ('description', 'eway_bill', 'consignment_invoice', 'packages', 'consignment_value', 'actual_weight', 'charged_weight', 'freight_charges')
        }),
        ('Billing Details', {
            'fields': ('invoice_number', 'other_charges', 'total_charge')
        }),
        ('Status', {
            'fields': ('delivery_status', 'payment_status')
        }),
    )

# PDF Generation using ReportLab Library!
