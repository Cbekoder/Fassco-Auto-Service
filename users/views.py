from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee, Supplier, Client
from .permissions import IsSameBranch
from .serializers import *
from .serializers import ManagerSerializer
from rest_framework.permissions import IsAuthenticated


class ManagerListCreateView(ListCreateAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='manager', branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(
            position="meneger",
            branch_id=self.request.user.branch_id
        )

class ManagerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='manager', branch_id=self.request.user.branch_id)


class MechanicListCreateView(ListCreateAPIView):
    serializer_class = MechanicSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='mechanic', branch_id=self.request.user.branch_id)


    def perform_create(self, serializer):
        serializer.save(
            position="mechanic",
            branch_id=self.request.user.branch_id
        )

class MechanicRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = MechanicSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='mechanic', branch_id=self.request.user.branch_id)


class WorkerListCreateView(ListCreateAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='other', branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(
            position="other",
            branch_id=self.request.user.branch_id
        )
class WorkerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Employee.objects.filter(position='other', branch_id=self.request.user.branch_id)


class SupplierListCreateView(ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Supplier.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierSerializer
        return SupplierPostSerializer


class SupplierRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Supplier.objects.filter(branch_id=self.request.user.branch_id)


class ClientListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientSerializer
        return ClientPostSerializer

    def get_queryset(self):
        return Client.objects.filter(branch_id=self.request.user.branch_id)

    def perform_create(self, serializer):
        serializer.save(branch_id=self.request.user.branch_id)


class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsSameBranch]

    def get_queryset(self):
        return Client.objects.filter(branch_id=self.request.user.branch_id)
