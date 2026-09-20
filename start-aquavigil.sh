#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"

command -v docker >/dev/null 2>&1 || { echo "Docker is not installed."; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker engine is not running."; exit 1; }
[ -f .env ] || cp .env.example .env

env_value() {
  value=$(sed -n "s/^$1=//p" .env | tail -n 1)
  printf '%s' "${value:-$2}"
}

APP_PORT_VALUE=$(env_value APP_PORT 8000)
PROMETHEUS_PORT_VALUE=$(env_value PROMETHEUS_PORT 9090)
GRAFANA_PORT_VALUE=$(env_value GRAFANA_PORT 3000)

docker compose down --remove-orphans
docker compose pull prometheus grafana
docker compose up --build --force-recreate -d

attempt=0
until [ "$attempt" -ge 60 ]; do
  if curl -fsS "http://localhost:${APP_PORT_VALUE}/health" 2>/dev/null | grep -q '"status":"ok"'; then
    break
  fi
  attempt=$((attempt + 1))
  sleep 2
done

if [ "$attempt" -ge 60 ]; then
  docker compose ps
  echo "AquaVigil did not become healthy within two minutes."
  exit 1
fi

echo "AquaVigil:  http://localhost:${APP_PORT_VALUE}"
echo "Prometheus: http://localhost:${PROMETHEUS_PORT_VALUE}"
echo "Grafana:    http://localhost:${GRAFANA_PORT_VALUE} (admin / aquavigil)"

if command -v open >/dev/null 2>&1; then open "http://localhost:${APP_PORT_VALUE}"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "http://localhost:${APP_PORT_VALUE}"
fi
