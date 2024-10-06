
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderService, OrderProduct
from .serializers import OrderSerializer, OrderServiceSerializer, OrderProductSerializer
from users.permissions import IsSameBranch  # Assuming permission for branch-level access

# Views for Order
class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Order.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)


class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Order.objects.filter(branch_id=self.request.user.branch_id)


class OrderServiceListCreateView(ListCreateAPIView):
    serializer_class = OrderServiceSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return OrderService.objects.filter(order_id__branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        order = serializer.validated_data['order_id']
        if order.branch_id != self.request.user.branch_id:
            raise ValidationError("You cannot add services to orders from other branches.")
        serializer.save()


class OrderServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderServiceSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return OrderService.objects.filter(order_id__branch_id=self.request.user.branch_id)


class OrderProductListCreateView(ListCreateAPIView):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return OrderProduct.objects.filter(order_id__branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        order = serializer.validated_data['order_id']
        if order.branch_id != self.request.user.branch_id:
            raise ValidationError("You cannot add products to orders from other branches.")
        serializer.save()


class OrderProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return OrderProduct.objects.filter(order_id__branch_id=self.request.user.branch_id)
