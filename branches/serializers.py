from rest_framework.serializers import ModelSerializer

from branches.models import Branch


class BranchBalanceSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'