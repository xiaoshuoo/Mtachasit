from rest_framework.routers import DefaultRouter
from .views import GutierrezTemplateViewSet, RossiTemplateViewSet


router = DefaultRouter()
router.register(r"templates", GutierrezTemplateViewSet, basename="gutierrez-template")
router.register(r"templates-rossi", RossiTemplateViewSet, basename="rossi-template")

urlpatterns = [
    *router.urls,
]


