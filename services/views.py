from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderPostSerializer, OrderListSerializer


class OrderListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderPostSerializer


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)
