from rest_framework import serializers
from ..models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        response_time_seconds = representation.pop('average_response_time')
        representation['average_response_time'] = f"{response_time_seconds} seconds"
        return representation