# external-api-consumer-service

External API Consumer Service

## Requisitos

- Python 3.9
- Postgres

## Instalação

### Via docker-compose

```shell
docker-compose build api
docker-compose run api python manage.py migrate
docker-compose run api python createsuperuser
```

### Via local pip

```shell
pip install -r requirements.txt
python manage.py migrate
python createsuperuser
```

## Uso

### Obtain Token Pair

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}' \
  http://localhost:8000/auth/token/obtain
```

```json
{
  "refresh": "...",
  "access": "..."
}
```

### List todo

```shell
curl \
  -X POST \
  -H 'Authorization: Bearer token' \
  http://localhost:8000/todos
```

```json
[
  { "id": 1, "title": "delectus aut autem" },
  { "id": 2, "title": "quis ut nam facilis et officia qui" },
  { "id": 3, "title": "fugiat veniam minus" },
  { "id": 4, "title": "et porro tempora" },
  {
    "id": 5,
    "title": "laboriosam mollitia et enim quasi adipisci quia provident illum"
  }
]
```

### Refresh Access Token

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh": "token"}' \
  http://localhost:8000/api/token/refresh/
```

```json
{
  "access": "token"
}
```
