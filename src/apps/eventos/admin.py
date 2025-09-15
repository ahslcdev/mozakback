# Register your models here.
from django.apps import apps
from django.contrib import admin

# Pega o app atual dinamicamente
app = apps.get_app_config("eventos")

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
