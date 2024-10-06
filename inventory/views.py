from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, Service, Car
from .serializers import ProductSerializer, ServiceSerializer, CarSerializer, ProductPostSerializer, \
    ServicePostSerializer, CarPostSerializer
from users.permissions import IsSameBranch, IsStaffStatus


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductPostSerializer

    def get_queryset(self):
        return Product.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(
            branch_id=self.request.user.branch_id
        )

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Product.objects.filter(branch_id=self.request.user.branch_id)


class ServiceListCreateView(ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsStaffStatus]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ServiceSerializer
        return ServicePostSerializer

    def get_queryset(self):
        return Service.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)


class ServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Service.objects.filter(branch_id=self.request.user.branch_id)


class CarListCreateView(ListCreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarSerializer
        return CarPostSerializer

    def get_queryset(self):
        return Car.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Car.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)