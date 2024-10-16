from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from branches.models import Branch
from branches.serializers import BranchBalanceSerializer


class BranchBalanceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={200: BranchBalanceSerializer},
        operation_description="Retrieve the balance of the authenticated user's branch."
    )
    def get(self, request):
        branch = Branch.objects.get(id=request.user.branch.id)
        serializer = BranchBalanceSerializer(branch)
        return Response(serializer.data)
