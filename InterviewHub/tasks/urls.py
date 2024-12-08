from rest_framework.routers import DefaultRouter
from .views.task_item_viewset import TaskItemViewSet
from .views.open_question_viewset import OpenQuestionViewSet
from .views.multiple_choice_question_viewset import MultipleChoiceQuestionViewSet
from .views.code_question_viewset import CodeQuestionViewSet

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
