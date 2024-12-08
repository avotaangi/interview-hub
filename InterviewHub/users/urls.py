from rest_framework.routers import DefaultRouter
from .views.auth_views import AuthViewSet
from .views.candidate_views import CandidateViewSet
from .views.company_views import CompanyViewSet
from .views.interviewer_views import InterviewerViewSet
from .views.user_views import UserViewSet

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"user", UserViewSet, basename="user")
router.register(r"candidates", CandidateViewSet, basename="candidates")
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"interviewers", InterviewerViewSet, basename="interviews")

urlpatterns = router.urls
