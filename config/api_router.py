from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from core.api import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('user', UserViewSet)

urlpatterns = router.urls
