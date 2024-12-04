from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.company_selection_views import CompanySelectionViewSet

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'company-selections', CompanySelectionViewSet, basename='company-selection')

urlpatterns = router.urls