# --- Setup ---

migrate-new NAME:
    docker exec -it user_pool_api alembic revision --autogenerate -m "{{NAME}}"

migrate-up:
    docker exec -it user_pool_api alembic upgrade head

migrate-down:
    docker exec -it user_pool_api alembic downgrade -1

env-create:
    cp ./configs/config/.env.dev.dist  ./configs/config/.env.dev
    cp ./configs/config/.env.test.dist ./configs/config/.env.test

    printf "DB_USER=\nDB_PASSWORD=\nDB_NAME=\n\nREDIS_PASSWORD=\n" > ./.env

gen-proto FILE_PATH:
    python3 -m grpc_tools.protoc -I configs/contracts \
    --python_out=src/user_pool/infrastructure/grpc/gen \
    --grpc_python_out=src/user_pool/infrastructure/grpc/gen \
    --mypy_out=src/user_pool/infrastructure/grpc/gen \
    --mypy_grpc_out=src/user_pool/infrastructure/grpc/gen \
    {{FILE_PATH}}

plot:
    PYTHONPATH=src uv run --env-file ./configs/config/.env.dev.dist ./scripts/plot_dependencies_data.py

# --- DEVELOPMENT ---

dev-build:
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build

dev-up:
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d

dev-down:
    docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down

# --- TESTING ---

test-up:
    docker compose -f docker-compose.yaml -f docker-compose.test.yaml up -d postgres redis

test-down:
    docker compose -f docker-compose.yaml -f docker-compose.test.yaml down
