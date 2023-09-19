from rest_framework import serializers

from .models import Wallet


class WalletInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "balance",
        ]
