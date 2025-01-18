from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .views.auth_views import AuthViewSet
from .views.candidate_views import CandidateViewSet
from .views.company_views import CompanyViewSet
from .views.interviewer_views import InterviewerViewSet
from .views.user_views import UserViewSet

from django.urls import path
from .views.template_views import register_view, login_view, home_candidate_view, home_interviewer_view, home_view, \
    custom_logout_view

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"user", UserViewSet, basename="user")
router.register(r"candidates", CandidateViewSet, basename="candidates")
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"interviewers", InterviewerViewSet, basename="interviews")

urlpatterns = router.urls

urlpatterns += [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),  # Маршрут для выхода
]

urlpatterns += [
    path('account/', login_required(home_view), name='account'),  # Общая страница аккаунта
    path('account/candidate/', login_required(home_candidate_view), name='home_candidate'),
    path('account/interviewer/', login_required(home_interviewer_view), name='home_interviewer'),
]
