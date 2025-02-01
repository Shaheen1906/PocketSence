from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonthlyExpenseAnalysisView, SettlementSuggestionView, StudentViewSet, GroupViewSet, CategoryViewSet, ExpenseViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'settlements', SettlementViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('monthly-analysis/', MonthlyExpenseAnalysisView.as_view(), name='monthly-analysis'),
    path('settlement-suggestions/', SettlementSuggestionView.as_view(), name='settlement-suggestions'),
]