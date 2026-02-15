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



4. Integration with an external SSO service

#### Setting up a gRPC client:

4.1. Change the host and port information in `configs/config/.env.*`

4.2. If you want to run the project locally, you can run a [local SSO server](). After installing, configuring, and launching the container, you need to create a network.

```shell
docker network create grpc_network
```

4.3. Copy the JWT public key file from the SSO application and specify the path in the config
4.4. Run API container (current repository)
4.5. Find out container names

```shell
docker ps
```

4.6. Connect containers to the shared network

```shell
docker network connect grpc_network auth-auth-1
docker network connect grpc_network user_pool_api
```
###### insert your container names

4.7. Restart containers

___

5. Create keys for nginx

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

### Running locally outside a Docker container

```shell
PYTHONPATH=src uv run --env-file configs/config/.env.* src/user_pool/setup/main.py
```