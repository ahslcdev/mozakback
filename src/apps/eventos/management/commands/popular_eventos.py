import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.eventos.models import Evento
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = (
        "Cria usuários IDs 1 a 4 (se não existirem) e gera eventos de teste para eles"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--total", type=int, default=20, help="Número de eventos a serem criados"
        )

    def handle(self, *args, **options):
        fake = Faker()
        total = options["total"]

        donos = []
        for i in range(1, 5):
            user, created = Usuario.objects.get_or_create(
                id=i,
                defaults={
                    "username": f"user{i}",
                    "email": f"user{i}@teste.com",
                },
            )
            donos.append(user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Usuário {user.username} criado (ID={user.id})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Usuário {user.username} já existe (ID={user.id})"
                    )
                )

        for i in range(total):
            dono = donos[i % len(donos)]

            comeca = timezone.now() + timedelta(
                days=random.randint(1, 30), hours=random.randint(0, 23)
            )
            termina = comeca + timedelta(hours=random.randint(1, 6))

            Evento.objects.create(
                fk_dono=dono,
                nome=fake.sentence(nb_words=3),
                descricao=fake.text(max_nb_chars=200),
                endereco=fake.street_name(),
                complemento=fake.secondary_address(),
                cep=fake.postcode(),
                numero=str(random.randint(1, 9999)),
                cidade=fake.city(),
                estado=fake.state(),
                comeca_as=comeca,
                termina_as=termina,
                max_inscricoes=random.randint(10, 100),
                is_ativo=random.choice([True, True, True, False]),
                uuid_code=fake.uuid4(),
            )

        self.stdout.write(self.style.SUCCESS(f"{total} eventos criados com sucesso!"))
