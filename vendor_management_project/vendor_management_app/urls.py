from django.urls import path
from .api.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management API",
      default_version='v1',
      description="API for managing vendors, purchase orders, and performance metrics.",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
  permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/vendors/', VendorListCreateView.as_view(), name='api_vendor_list_create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='api_vendor_retrieve_update_destroy'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='api_purchase_order_list_create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='api_purchase_order_retrieve_update_destroy'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='api_vendor_performance'),
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='api_acknowledge_po'),
]