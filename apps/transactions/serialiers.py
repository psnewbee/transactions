from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from .models import UserCategory, Transaction, UserTransaction
from apps.wallets.models import Wallet
from extentions import exceptions, TransactionStatusEnum, TransactionTypesEnum


class TransactionUpdateCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(min_value=1)

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCategory
        fields = ['id', 'title',]
    
    def create(self, validated_data):
        user_id = self.context["user_id"]
        title = validated_data.get('title')

        if UserCategory.objects.filter(user__id=user_id, title=title).exists():
            raise exceptions.AlreadyExist(detail=f"Category '{title}' is already exist")
        
        return UserCategory.objects.create(user_id=user_id, title=title)


class TransactionInfoSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'status', 'type', 'category')



class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'status', 'type', 'category',)
        read_only_fields = ('status', 'type', 'category')
    
    def create(self, validated_data):
        user_id = self.context.pop('user_id')
        cashflow = validated_data.get('amount')
        wallet = Wallet.objects.get(user__id=user_id)
        
        if self.context.get('type') == TransactionTypesEnum.outcome.value:
            if not wallet.check_wallet_solvency(cashflow):
                validated_data['status'] = TransactionStatusEnum.unsuccessful.value
            else:
                wallet.balance -= cashflow
        else:
            wallet.balance += cashflow
        wallet.save()

        created_transaction = Transaction.objects.create(**validated_data, **self.context)
        UserTransaction.objects.create(user_id=user_id, transaction=created_transaction)
        
        return created_transaction
