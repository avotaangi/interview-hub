from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.skill_views import SkillViewSet
from .views.resume_views import ResumeViewSet
from .views.job_views import JobViewSet

router = DefaultRouter()
router.register(r'skill', SkillViewSet)
router.register(r'resume', ResumeViewSet)
router.register(r'job_experience', JobViewSet)

urlpatterns = router.urls