# admin.py

from django.contrib import admin
from .admin import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from .models import *
from import_export.admin import *
from import_export import resources




class VendorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('name', 'vendor_code')


class PurchaseOrderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date')
    list_filter = ('po_number', 'vendor__name')

class HistoricalPerformanceAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('vendor__name', 'date')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)