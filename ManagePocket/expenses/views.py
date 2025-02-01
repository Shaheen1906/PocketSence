from rest_framework import viewsets
from .models import Student, Group, Category, Expense, Settlement
from .serializers import StudentSerializer, GroupSerializer, CategorySerializer, ExpenseSerializer, SettlementSerializer
from django.db.models import Sum
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Settlement.objects.filter(payer=self.request.user)


class MonthlyExpenseAnalysisView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Extract user from token
        user = request.user

        # Extract date from query params (format: YYYY-MM)
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Date parameter is required (format: YYYY-MM)"}, status=400)

        try:
            year, month = map(int, date_str.split('-'))
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM."}, status=400)

        # Calculate total expenses for the given month
        total_expense = Expense.objects.filter(
            paid_by=user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "user_id": user.id,
            "month": month,
            "year": year,
            "total_expense": total_expense
        })

class SettlementSuggestionView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get group_id from query params
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response({"error": "Group ID is required"}, status=400)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=404)

        members = group.members.all()

        # Initialize balances for each user
        balances = {member.id: 0 for member in members}

        # Calculate balances
        for expense in group.expenses.all():
            split_amount = expense.amount / len(members)
            
            # Subtract expense from all members
            for member in members:
                balances[member.id] -= split_amount
            
            # Ensure `paid_by` is in balances before adding
            if expense.paid_by.id in balances:
                balances[expense.paid_by.id] += expense.amount
            else:
                return Response({"error": f"User {expense.paid_by.username} is not in the group"}, status=400)

        # Suggest payments
        suggestions = []
        for payer_id, amount in balances.items():
            if amount < 0:
                for payee_id, payee_amount in balances.items():
                    if payee_amount > 0:
                        suggested_amount = min(-amount, payee_amount)
                        suggestions.append({
                            "payer": Student.objects.get(id=payer_id).username,
                            "payee": Student.objects.get(id=payee_id).username,
                            "amount": suggested_amount
                        })
                        balances[payer_id] += suggested_amount
                        balances[payee_id] -= suggested_amount

        return Response(suggestions)