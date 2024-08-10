from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.routers import DefaultRouter
from .views import CustomerListCreate, CustomerRetrieveUpdateDestroy, PhlaboViewSet, BookingViewSet, TestsViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'phlabos', PhlaboViewSet)
router.register(r'tests', TestsViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('customers/', CustomerListCreate.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroy.as_view(), name='customer-detail'),
    path('', include(router.urls)),
]
