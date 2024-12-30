from django.urls import path
from .views import example_view, example_context_variable, example_queryset

urlpatterns = [
    path('queryset/example/', example_queryset, name='example_queryset'),
    path('tag/example/', example_view, name='example_view'),
    path('context/example/', example_context_variable, name='example_context_variable'),
]
