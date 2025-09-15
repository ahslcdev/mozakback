from rest_framework.routers import DefaultRouter

from api.eventos.viewsets import EventoAdminViewSet, EventoSiteViewSet

router = DefaultRouter()
router.register(r"admin/eventos", EventoAdminViewSet, basename="eventos-admin")
router.register(r"eventos", EventoSiteViewSet, basename="eventos-site")

urlpatterns = [*router.urls]
