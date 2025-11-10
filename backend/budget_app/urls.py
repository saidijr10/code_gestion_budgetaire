from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrestataireViewSet,
    RIBViewSet,
    BudgetViewSet,
    DepensesBudgetViewSet,
    LigneBudgetaireViewSet,
    OrdonnancementViewSet,
    ReglementViewSet,
    CodeBanqueViewSet,
    CodeLocaliteViewSet,
    exporter_budget_excel,
    ImportBudgetView
)

router = DefaultRouter()
router.register(r'prestataires', PrestataireViewSet)
router.register(r'ribs', RIBViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'budgets-depenses', DepensesBudgetViewSet, basename='budgets-depenses')
router.register(r'ligne-budgetaire', LigneBudgetaireViewSet)
router.register(r'ordonnancements', OrdonnancementViewSet)
router.register(r'reglements', ReglementViewSet)
router.register(r'codebanques', CodeBanqueViewSet, basename='codebanque')
router.register(r'codelocalites', CodeLocaliteViewSet, basename='codelocalite')

urlpatterns = [
    path('', include(router.urls)),
    path('export-budget/<int:annee>/<str:type_budget>/', exporter_budget_excel, name='export-budget'),
    path('import-budget/', ImportBudgetView.as_view(), name='import-budget'),
]
