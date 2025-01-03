from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.company_selection_views import CompanySelectionViewSet
from .views.template_company_selection import company_selection_create, company_selection_view, \
    company_selection_success

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(
    r"company-selections", CompanySelectionViewSet, basename="company-selection"
)

urlpatterns = router.urls

urlpatterns += [
    path('selections/create', company_selection_create, name='company_selection_create'),
    path('selections/', company_selection_view, name='company_selection'),
    path('selections/<int:pk>/', company_selection_view, name='edit_company_selection'),
    path('selections/success/', company_selection_success, name='company_selection_success'),
]
