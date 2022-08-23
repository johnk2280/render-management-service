#!/bin/sh
# wait-for-psql.sh

set -e

shift

sleep 5

>&2 echo "Postgres is up - executing command"
exec "$@"
