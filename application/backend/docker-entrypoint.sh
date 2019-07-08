#!/bin/sh

mkdir -p /run/secrets/
echo "my-db-pass" > /run/secrets/secret-db-pass
export DB_HOST=my-db-host
export DB_USER=my-db-user
export DB_PASS={{DOCKER-SECRET:secret-db-pass}}

source /app/env_secrets_expand.sh

exec "$@"
