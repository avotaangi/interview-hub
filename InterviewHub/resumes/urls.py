from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.skill_views import SkillViewSet
from .views.resume_views import ResumeViewSet
from .views.job_views import JobViewSet
from .views.template_views import resume_interviewer_view

router = DefaultRouter()
router.register(r"skill", SkillViewSet)
router.register(r"resume", ResumeViewSet)
router.register(r"job_experience", JobViewSet)

urlpatterns = router.urls


urlpatterns += [
    # Другие маршруты...
    path("resumedata/interviewer/", resume_interviewer_view, name="resume_interviewer"),
]