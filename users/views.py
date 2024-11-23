from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, Supplier, Client
from .permissions import IsSameBranch, IsAdminUser
from .serializers import *
from .serializers import ManagerSerializer
from rest_framework.permissions import IsAuthenticated


class GetMeAPIView(APIView):
    permission_classes = [IsAdminUser,]
    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_description="Retrieve the authenticated user."
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class SupplierListCreateView(ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        return Supplier.objects.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierSerializer
        return SupplierPostSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        supplier = self.get_queryset().get(pk=response.data['id'])
        response_data = SupplierSerializer(supplier).data
        return Response(response_data, status=status.HTTP_201_CREATED)

class SupplierRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Supplier.objects.filter(branch=self.request.user.branch)
        return



class ManagerListCreateView(ListCreateAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='manager', branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(
            position="manager",
            branch=self.request.user.branch
        )

class ManagerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.filter(position='manager')
    serializer_class = ManagerSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class MechanicListCreateView(ListCreateAPIView):
    queryset = Employee.objects.filter(position='mechanic')
    serializer_class = MechanicSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(
            position="mechanic",
            branch=self.request.user.branch
        )

class MechanicRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.filter(position='mechanic')
    serializer_class = MechanicSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class WorkerListCreateView(ListCreateAPIView):
    queryset = Employee.objects.filter(position='other')
    serializer_class = WorkerSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(
            position="other",
            branch=self.request.user.branch
        )
class WorkerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.filter(position='other')
    serializer_class = WorkerSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

class ClientListCreateView(ListCreateAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientSerializer
        return ClientPostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()


class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser, IsSameBranch]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return self.queryset.none()
