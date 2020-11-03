#!/bin/bash
export PGPASSWORD='docker'
until psql -h localhost -U docker -d qalert_test -c "select 1" > /dev/null 2>&1; do
  echo "Waiting for postgres server..."
  sleep 1
done