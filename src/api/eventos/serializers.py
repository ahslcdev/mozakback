from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.eventos.models import Evento, EventoUsuario


class EventoListSerializer(ModelSerializer):
    is_inscrito = SerializerMethodField()
    class Meta:
        model = Evento
        fields = ["id", "uuid_code", "comeca_as", "nome", "endereco_evento", "is_ativo", 'is_inscrito', ]

    def get_is_inscrito(self, obj: Evento):
        is_inscrito = False
        usuario = self.context.get('request').user

        if not usuario.is_anonymous and obj.eventousuario_set.filter(
            deletado_em=None, 
            fk_usuario=usuario
        ).exists():
            is_inscrito = True
        return is_inscrito

class EventoCreateSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = [
            "uuid_code",
            "fk_dono",
            "nome",
            "descricao",
            "endereco",
            "complemento",
            "cep",
            "numero",
            "cidade",
            "estado",
            "comeca_as",
            "termina_as",
            "max_inscricoes",
            "is_ativo",
        ]

    def validate(self, attrs):
        comeca_as = attrs.get('comeca_as')
        termina_as = attrs.get('termina_as')
        if comeca_as and termina_as <= DateTimeField().to_internal_value(comeca_as):
            raise ValidationError({
                "detail": "O horário de término deve ser posterior ao horário de início."
            })
        return attrs

    def validate_cep(self, attrs):
        cep = attrs.replace("-", "").replace(".", "")
        return cep

    def create(self, validated_data):
        evento = super().create(validated_data)
        EventoUsuario.objects.create(
            fk_evento=evento, fk_usuario=self.context.get("request").user
        )
        return evento


class EventoRetrieveSerializer(ModelSerializer):
    is_inscrito = SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            "id",
            "uuid_code",
            "nome",
            "descricao",
            "endereco_evento",
            "endereco",
            "complemento",
            "cep",
            "numero",
            "cidade",
            "estado",
            "comeca_as",
            "termina_as",
            "max_inscricoes",
            "is_ativo",
            'is_inscrito'
        ]
    
    def get_is_inscrito(self, obj: Evento):
        is_inscrito = False
        usuario = self.context.get('request').user

        if not usuario.is_anonymous and obj.eventousuario_set.filter(
            deletado_em=None, 
            fk_usuario=usuario
        ).exists():
            is_inscrito = True
        return is_inscrito


class EventoPatchSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = [
            "nome",
            "descricao",
            "endereco",
            "complemento",
            "cep",
            "numero",
            "cidade",
            "estado",
            "comeca_as",
            "termina_as",
            "max_inscricoes",
            "is_ativo",
        ]

    def validate(self, attrs):
        comeca_as = attrs.get('comeca_as')
        termina_as = attrs.get('termina_as')
        if comeca_as and termina_as <= DateTimeField().to_internal_value(comeca_as):
            raise ValidationError({
                "detail": "O horário de término deve ser posterior ao horário de início."
            })
        return attrs

    def validate_cep(self, attrs):
        cep = attrs.replace("-", "").replace(".", "")
        return cep


class EventoUsuarioInscreverSerializer(ModelSerializer):
    def validate(self, data):
        evento = data.get("fk_evento")
        usuario = data.get("fk_usuario")
        if not evento.is_ativo:
            raise ValidationError({"detail": "Evento inativo."})
        if evento.termina_as <= timezone.now():
            raise ValidationError({"detail": "Evento já terminou."})
        if evento.eventousuario_set.count() >= evento.max_inscricoes:
            raise ValidationError({
                "detail": "Evento já atingiu o limite de inscrições."
            })
        if EventoUsuario.objects.filter(
            fk_usuario=usuario, fk_evento__termina_as__gt=timezone.now()
        ).exclude(fk_evento__fk_dono=usuario).exists():
            raise ValidationError({
                "detail": "Usuário já está inscrito em outro evento."
            })
        return data

    class Meta:
        fields = ["fk_usuario", "fk_evento"]
        model = EventoUsuario
