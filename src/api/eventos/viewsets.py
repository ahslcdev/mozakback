from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.eventos.filters import EventoAdminFilter, EventoSiteFilter
from api.eventos.serializers import (
    EventoCreateSerializer,
    EventoListSerializer,
    EventoPatchSerializer,
    EventoRetrieveSerializer,
    EventoUsuarioInscreverSerializer,
)
from apps.eventos.models import Evento


class EventoAdminViewSet(ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoListSerializer
    filterset_class = EventoAdminFilter
    http_method_names = ["get", "post", "delete", "patch"]
    search_fields = ["nome", "descricao", "endereco", "estado", "cidade", "cep"]
    lookup_field = "uuid_code"

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.action == "create":
            serializer = EventoCreateSerializer
        elif self.action == "retrieve":
            serializer = EventoRetrieveSerializer
        elif self.action == "partial_update":
            serializer = EventoPatchSerializer
        return serializer

    def get_queryset(self):
        return super().get_queryset().filter(fk_dono=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["fk_dono"] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=204)


class EventoSiteViewSet(ModelViewSet):
    queryset = Evento.objects.filter(is_ativo=True)
    serializer_class = EventoListSerializer
    http_method_names = ["get", "post", "patch"]
    filterset_class = EventoSiteFilter
    search_fields = ["nome", "descricao", "endereco", "estado", "cidade", "cep"]
    lookup_field = "uuid_code"

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            method=request.method,
            detail=f"O método {request.method} não é permitido neste recurso.",
        )

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            method=request.method,
            detail=f"O método {request.method} não é permitido neste recurso.",
        )

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return []
        return super().get_permissions()

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.action == "inscrever":
            serializer = EventoUsuarioInscreverSerializer
        elif self.action == "retrieve":
            serializer = EventoRetrieveSerializer
        return serializer

    @action(methods=["POST"], url_path="inscrever", detail=True)
    def inscrever(self, request, *args, **kwargs):
        evento = self.get_object()
        data = {"fk_usuario": request.user.id, "fk_evento": evento.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": f"Você foi inscrito no evento: {evento.nome}"})

    @action(methods=["PATCH"], url_path="cancelar-inscricao", detail=True)
    def cancelar_inscricao(self, request, *args, **kwargs):
        evento = self.get_object()
        evento_usuario = evento.eventousuario_set.filter(
            fk_usuario=request.user, deletado_em=None
        )
        if not evento_usuario.exists():
            return Response({"detail": "Você não está associado a este evento."})
        evento_usuario.last().delete()
        return Response({
            "msg": f"Sua inscrição para o evento {evento.nome} foi cancelada."
        })
