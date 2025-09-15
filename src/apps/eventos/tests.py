from datetime import datetime, timedelta
from django.test import TestCase

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from rest_framework.test import APIClient
from rest_framework import status

from apps.eventos.models import Evento, EventoUsuario
from apps.usuarios.models import Usuario


class EventoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = Usuario.objects.create_user(username="user1", password="123456")
        self.user2 = Usuario.objects.create_user(username="user2", password="123456")

        self.agora = make_aware(datetime.now())
        self.depois = self.agora + timedelta(hours=2)

        self.evento1 = Evento.objects.create(
            nome="Evento Teste 1",
            descricao="desc",
            endereco="rua x",
            complemento="",
            numero="123",
            estado="SP",
            cidade="São Paulo",
            cep="00000-000",
            fk_dono=self.user1,
            comeca_as=self.agora,
            termina_as=self.depois,
            max_inscricoes=100,
            is_ativo=True,
        )

        self.evento2 = Evento.objects.create(
            nome="Evento Teste 2",
            descricao="desc2",
            endereco="rua y",
            complemento="",
            numero="456",
            estado="RJ",
            cidade="Rio",
            cep="11111-111",
            fk_dono=self.user2,
            comeca_as=self.agora,
            termina_as=self.depois,
            max_inscricoes=50,
            is_ativo=True,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_list_eventos_admin_apenas_dono(self):
        self.authenticate(self.user1)
        response = self.client.get("/api/admin/eventos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.json().get('results')]
        self.assertIn(self.evento1.id, ids)
        self.assertNotIn(self.evento2.uuid_code, ids)

    def test_create_evento_admin_define_dono(self):
        self.authenticate(self.user1)
        response = self.client.post("/api/admin/eventos/", {
            "nome": "Novo Evento",
            "descricao": "desc",
            "endereco": "rua z",
            "complemento": "",            
            "numero": "123",            
            "estado": "MG",
            "cidade": "Belo Horizonte",
            "cep": "22222-222",
            "comeca_as": self.agora.isoformat(),     
            "termina_as": self.depois.isoformat(),   
            "max_inscricoes": 100,
            "is_ativo": True,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["fk_dono"], self.user1.id)

    def test_update_evento_apenas_dono(self):
        self.authenticate(self.user2)
        response = self.client.patch(f"/api/admin/eventos/{self.evento1.uuid_code}/", {
            "nome": "Hackeado"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.authenticate(self.user1)
        response = self.client.patch(f"/api/admin/eventos/{self.evento1.uuid_code}/", {
            "nome": "Editado"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["nome"], "Editado")

    def test_delete_evento_apenas_dono(self):
        self.authenticate(self.user2)
        response = self.client.delete(f"/api/admin/eventos/{self.evento1.uuid_code}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.authenticate(self.user1)
        response = self.client.delete(f"/api/admin/eventos/{self.evento1.uuid_code}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_inscrever_evento_autenticado(self):
        self.authenticate(self.user1)
        response = self.client.post(f"/api/eventos/{self.evento2.uuid_code}/inscrever/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(EventoUsuario.objects.filter(fk_usuario=self.user1, fk_evento=self.evento2).exists())

    def test_inscrever_evento_nao_autenticado(self):
        response = self.client.post(f"/api/eventos/{self.evento1.uuid_code}/inscrever/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancelar_inscricao_autenticado(self):
        EventoUsuario.objects.create(fk_usuario=self.user1, fk_evento=self.evento2)

        self.authenticate(self.user1)
        response = self.client.patch(f"/api/eventos/{self.evento2.uuid_code}/cancelar-inscricao/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(EventoUsuario.objects.filter(fk_usuario=self.user1, fk_evento=self.evento2).exists())

    def test_cancelar_inscricao_sem_participacao(self):
        self.authenticate(self.user1)
        response = self.client.patch(f"/api/eventos/{self.evento2.uuid_code}/cancelar-inscricao/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Você não está associado a este evento", response.json()["detail"])

    def test_cancelar_inscricao_nao_autenticado(self):
        response = self.client.patch(f"/api/eventos/{self.evento2.uuid_code}/cancelar-inscricao/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
