from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.task_item_viewset import TaskItemViewSet
from .views.open_question_viewset import OpenQuestionViewSet
from .views.multiple_choice_question_viewset import MultipleChoiceQuestionViewSet
from .views.code_question_viewset import CodeQuestionViewSet
from .views.template_views import *

router = DefaultRouter()
router.register(r"task-items", TaskItemViewSet, basename="taskitem")
router.register(r"open-questions", OpenQuestionViewSet, basename="openquestion")
router.register(
    r"multiple-choice-questions",
    MultipleChoiceQuestionViewSet,
    basename="multiplechoicequestion",
)
router.register(r"code-questions", CodeQuestionViewSet, basename="codequestion")

urlpatterns = router.urls

urlpatterns += [
    path('tasks/choices/', tasks_with_choices, name='tasks_with_choices'),
    path('tasks/open/', tasks_with_open_questions, name='tasks_with_open_questions'),
    path('tasks/code/', tasks_with_code_questions, name='tasks_with_code_questions'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/', all_tasks, name='all_tasks'),

]
