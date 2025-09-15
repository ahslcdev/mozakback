import uuid
from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware

from apps.base.manages import SoftDeleteManager


class BaseModel(models.Model):
    uuid_code = models.CharField(
        max_length=128, unique=True, null=True, blank=True, default=uuid.uuid4
    )
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("Data de atualização", auto_now=True)
    deletado_em = models.DateTimeField("Data de deleção", null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deletado_em = make_aware(datetime.now())
        self.save()
