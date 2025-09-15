from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.eventos"
    verbose_name = "Eventos"

    def ready(self):
        # inicializa firebase quando o app carrega
        from integracoes.firebase.api import initialize_firebase

        initialize_firebase()
