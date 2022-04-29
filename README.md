### Services

-   Centrifugo - 8000 port
-   FastApi - 5000 port
-   Frontend - 8080 port

### Run all services

```
docker compose up -d
```

### View logs

```
docker compose logs -f centrifugo
docker compose logs -f api
docker compose logs -f web
```

### View admin password in config.json file

```
docker compose exec centrifugo sh
cat config.json
```

### Use admin interface

```
http://localhost:8000
```
