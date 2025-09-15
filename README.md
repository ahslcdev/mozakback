# Projeto Django

## Clone o repositório

```
git clone https://github.com/ahslcdev/mozakfront
```

## Configure o .env

```env
FIREBASE_JSON_PATH=src/core/firebase/firebase.json
```
## Rodar o projeto com docker
```
docker-compose up --build
docker-compose exec api_eventos python manage.py migrate
docker-compose exec api_eventos python manage.py createsuperuser
docker-compose exec api_eventos python manage.py popular_eventos --total=50
```

## Rodar o projeto sem docker

### OBS: Para rodar com SQLite, basta descomentar a configuração no settings.py. Caso contrário, configure o PostgreSQL localmente.
```
python -m venv venv
source venv/bin/activate
venv\Scripts\activate

cd src/
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py popular_eventos --total=50
python manage.py runserver
```
