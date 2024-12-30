from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.interview_viewset import InterviewViewSet
from .views.interview_task_viewset import InterviewTaskItemViewSet
from .views.template_views import interview_list_view, interview_create_view, interview_edit_view, interview_delete_view

router = DefaultRouter()
router.register(r"interviews", InterviewViewSet, basename="interview")
router.register(r"interview-tasks", InterviewTaskItemViewSet, basename="interview-task")

urlpatterns = router.urls
urlpatterns += [
    path('interviews/show/list', interview_list_view, name='interview_list'),
    path('interviews/new', interview_create_view, name='interview_create'),
    path('interviews/<int:pk>/edit', interview_edit_view, name='interview_edit'),
    path('interviews/<int:pk>/delete', interview_delete_view, name='interview_delete'),
]
