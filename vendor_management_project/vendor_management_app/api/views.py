from django.db.models import F, DurationField
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from vendor_management_app.models import Vendor, PurchaseOrder
from django.db.models import Avg
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def calculate_performance_metrics(self, vendor):
        # On-Time Delivery Rate
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivery_rate = completed_pos.filter(delivery_date__lte=F('delivery_date')).count() / completed_pos.count() if completed_pos.count() > 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate

        # Quality Rating Average
        quality_ratings = completed_pos.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
        quality_rating_avg = quality_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] if quality_ratings else 0
        vendor.quality_rating_avg = quality_rating_avg

        # Average Response Time
        acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = []
        for pos in acknowledged_pos:
            if pos.acknowledgment_date and pos.issue_date:
                response_times.append((pos.acknowledgment_date - pos.issue_date).total_seconds())
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            vendor.average_response_time = average_response_time

        # Fulfillment Rate
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', issue_date__isnull=False)
        fulfillment_rate = fulfilled_pos.count() / PurchaseOrder.objects.filter(vendor=vendor).count() if PurchaseOrder.objects.filter(vendor=vendor).count() > 0 else 0
        vendor.fulfillment_rate = fulfillment_rate

        vendor.save()

    def get_object(self):
        vendor = super().get_object()
        self.calculate_performance_metrics(vendor)
        return vendor

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()
        po.save()
        vendor = po.vendor
        if hasattr(vendor, 'calculate_performance_metrics'):
            vendor.calculate_performance_metrics()
            vendor.save()
        return Response({'message': 'PO acknowledged successfully'})

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    # permission_classes = [permissions.IsAuthenticated]