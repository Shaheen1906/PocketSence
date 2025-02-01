from rest_framework import serializers
from .models import  Student, Group, Category, Expense, Settlement
from django.contrib.auth.hashers import make_password


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'password', 'college', 'semester', 'default_payment_method', 'upi_id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['id', 'expense', 'payer', 'payee', 'amount', 'payment_status', 'settlement_method', 'due_date']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        split_type = validated_data.get('split_type')
        amount = validated_data.get('amount')
        group = validated_data.get('group')
        paid_by = validated_data.get('paid_by')
        date = validated_data.get('date')
        split_details = validated_data.get('split_details', {})

        # Create the expense
        expense = Expense.objects.create(**validated_data)

        # Handle equal split
        if split_type == 'EQUAL':
            members = group.members.all()
            split_amount = amount / len(members)
            for member in members:
                if member != paid_by:
                    Settlement.objects.create(
                        expense=expense,
                        payer=member,
                        payee=paid_by,
                        amount=split_amount,
                        payment_status='PENDING',
                        settlement_method='UPI',  # Default method
                        due_date=date
                    )

        # Handle unequal split
        elif split_type == 'UNEQUAL':
            if not split_details:
                raise serializers.ValidationError("Split details are required for unequal splits.")

            for member_id, member_amount in split_details.items():
                member = Student.objects.get(id=member_id)
                if member != paid_by:
                    Settlement.objects.create(
                        expense=expense,
                        payer=member,
                        payee=paid_by,
                        amount=member_amount,
                        payment_status='PENDING',
                        settlement_method='UPI',  # Default method
                        due_date=date
                    )

        return expense