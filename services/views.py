from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdminUser
from .models import Order
from .serializers import OrderPostSerializer, OrderListSerializer


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser,]
    serializer_class = OrderPostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderPostSerializer


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser,]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()