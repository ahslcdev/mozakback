from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deletado_em=now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deletado_em__isnull=True)

    def dead(self):
        return self.exclude(deletado_em__isnull=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()