from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor_management_app.models import PurchaseOrder
from vendor_management_app.models import Vendor

@receiver(post_save, sender=PurchaseOrder)
def calculate_performance_metrics_on_save(sender, instance, **kwargs):
    if instance.status in ['completed', 'other_status_if_needed']:
        instance.vendor.calculate_performance_metrics()
        instance.vendor.save()