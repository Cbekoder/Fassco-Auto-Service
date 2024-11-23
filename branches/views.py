from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from branches.models import Branch
from branches.serializers import BranchBalanceSerializer
from users.serializers import UserSerializer


class BranchBalanceAPIView(APIView):
    permission_classes = [IsAdminUser,]
    @swagger_auto_schema(
        responses={200: BranchBalanceSerializer},
        operation_description="Retrieve the balance of the authenticated user's branch."
    )
    def get(self, request):
        if request.user.is_authenticated:
            branch = Branch.objects.get(id=request.user.branch.id)
            serializer = BranchBalanceSerializer(branch)
            response = serializer.data
            response['user'] = UserSerializer(request.user).data
            return Response(response)
