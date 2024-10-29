from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Product, Service, Car
from .serializers import ProductSerializer, ServiceSerializer, CarSerializer
from users.permissions import IsSameBranch, IsAdminUser


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(
            branch=self.request.user.branch
        )

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class ServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='client_id',
                in_=openapi.IN_QUERY,
                description="Filter by Client ID",
                type=openapi.TYPE_NUMBER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = self.queryset.filter(branch=self.request.user.branch).order_by('-created_at')
            client_id = self.request.query_params.get('client_id')
            if client_id:
                queryset = queryset.filter(client__id=client_id)
            return queryset
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()