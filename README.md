# User Pool service for e2e-tests

Available paths: [Swagger](https://localhost/docs) [Grafana](https://localhost/grafana)

## Launching the application


### 1. Set up environment variables

1. Create .env files `just env-create`
2. Set up environment variables for docker

###### Environment variables for docker dev mode (Example)

```
# ./env

DB_USER=my_user
DB_PASSWORD=my_pass
DB_NAME=user_pool

REDIS_PASSWORD=supersecret
```

3. Setting up environment variables for the application configuration
   - `./configs/config/config.yaml` 
   - `./configs/config/.env.dev`
   - `./configs/config/.env.test`


> For docker test mode, environment variables are taken from the same file as the application itself.


4. Create keys for nginx

```shell
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \                                                            
-keyout configs/nginx/certs/privkey.pem \
-out configs/nginx/certs/fullchain.pem \
-subj "/C=DE/ST=Hesse/L=Frankfurt/O=Dev/CN=localhost"
```

### 2. Run docker compose and run migrations (Dev mode)

```shell
just dev-up
```

Wait until the containers are ready to work and apply the migration (the first migration has already been created)

```shell
just migrate-up
```


### 3. Grafana settings

1. Go to [address](https://localhost/grafana)
2. Log in `admin: admin`
3. Create a new dashboard and import the json schema from `configs/grafana/dashboards/fastapi-dashboard.json`


## Application testing

Dependencies need to be installed

```shell
uv pip install --group test
```

### Running a Docker container for e2e tests

```shell
just test-up
```

> Only postgres and redis are running; ports are open

## Scripts

### View the dependency delivery schedule

1. Execute script

```shell
just plot
```

2. Copy the finished HTML page
3. Create an HTML file anywhere and paste the generated content

