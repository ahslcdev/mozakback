from django_filters import BooleanFilter, DateFilter, FilterSet

from apps.eventos.models import Evento


class BaseEventoFilter(FilterSet):
    data_inicio = DateFilter("comeca_as__date", "exact")
    data_termino = DateFilter("termina_as__date", "exact")


class EventoAdminFilter(BaseEventoFilter):
    is_ativo = BooleanFilter("is_ativo", "exact")

    class Meta:
        fields = ["data_inicio", "data_termino", "is_ativo"]
        model = Evento


class EventoSiteFilter(BaseEventoFilter):
    class Meta:
        fields = ["data_inicio", "data_termino"]
        model = Evento
