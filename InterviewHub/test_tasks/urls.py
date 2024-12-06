from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.test_task_views import TestTaskViewSet
from .views.test_task_item_views import TestTaskItemViewSet

# Создаем роутер для автоматической генерации маршрутов
router = DefaultRouter()
router.register(r"test-tasks", TestTaskViewSet, basename="test-task")
router.register(r"test-task-items", TestTaskItemViewSet, basename="test-task-item")

urlpatterns = router.urls
