from django.db import models

from apps.base.models import BaseModel
from apps.usuarios.models import Usuario


class Evento(BaseModel):
    fk_dono = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Dono")
    nome = models.CharField("Nome", max_length=255)
    descricao = models.TextField("Descrição", blank=True)
    endereco = models.CharField("Endereço", max_length=255)
    complemento = models.CharField("Complemento", max_length=255, blank=True)
    cep = models.CharField("Cep", max_length=20)
    numero = models.CharField("Número", max_length=20)
    cidade = models.CharField("Cidade", max_length=100)
    estado = models.CharField("Estado", max_length=100)
    comeca_as = models.DateTimeField("Horário que começa")
    termina_as = models.DateTimeField("Horário que termina")
    max_inscricoes = models.PositiveIntegerField("Máximo de inscrições permitidas")
    is_ativo = models.BooleanField("Está ativo?", default=True)

    def __str__(self):
        return self.nome

    @property
    def endereco_evento(self):
        return (
            f"{self.endereco} {self.numero} {self.complemento} "
            f"{self.cidade} {self.estado} {self.cep}"
        )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class EventoUsuario(BaseModel):
    fk_evento = models.ForeignKey(
        Evento, on_delete=models.CASCADE, verbose_name="Evento"
    )
    fk_usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuário"
    )

    class Meta:
        verbose_name = "Evento e convidado"
        verbose_name_plural = "Eventos e convidados"

    def __str__(self):
        return f"{self.fk_usuario.username} - {self.fk_evento.nome}"
