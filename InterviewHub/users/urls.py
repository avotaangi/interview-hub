from rest_framework.routers import DefaultRouter
from .views.auth_views import AuthViewSet
from .views.user_views import UserViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
