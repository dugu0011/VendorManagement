# models.py
from django.db import models
import json
from django.utils import timezone
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


    def calculate_performance_metrics(self):
        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        self.quality_rating_avg = self.calculate_quality_rating_avg()
        self.average_response_time = self.calculate_average_response_time()
        self.fulfillment_rate = self.calculate_fulfillment_rate()

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        return on_time_pos.count() / completed_pos.count() if completed_pos.count() > 0 else 0

    def calculate_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        quality_ratings = completed_pos.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
        return sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        response_times = [pos.acknowledgment_date - pos.issue_date for pos in acknowledged_pos]
        return sum(response_times, timedelta()) / len(response_times) if response_times else timedelta()

    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.all()
        fulfilled_pos = total_pos.filter(status='completed', issues__isnull=True)
        return fulfilled_pos.count() / total_pos.count() if total_pos.count() > 0 else 0

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"