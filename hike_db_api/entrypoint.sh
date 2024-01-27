#!/bin/sh

#!/bin/sh
# entrypoint.sh

cmd="$@"

echo "Waiting for postgres..."

while ! nc -z mountains 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

flask db upgrade
exec "$@"