#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"

command -v docker >/dev/null 2>&1 || { echo "Docker is not installed."; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker engine is not running."; exit 1; }
[ -f .env ] || cp .env.example .env
# Earlier distributions erased history at startup; migrate that setting safely.
if grep -q '^AQUAVIGIL_RESET_ON_START=1$' .env; then
  sed 's/^AQUAVIGIL_RESET_ON_START=1$/AQUAVIGIL_RESET_ON_START=0/' .env > .env.aquavigil.tmp
  mv .env.aquavigil.tmp .env
fi

env_value() {
  value=$(sed -n "s/^$1=//p" .env | tail -n 1)
  printf '%s' "${value:-$2}"
}

APP_PORT_VALUE=$(env_value APP_PORT 8000)
PROMETHEUS_PORT_VALUE=$(env_value PROMETHEUS_PORT 9090)
GRAFANA_PORT_VALUE=$(env_value GRAFANA_PORT 3000)
if [ "$(env_value MQTT_ENABLED 0)" = 1 ]; then
  set -- --profile simulator
else
  set --
fi

docker compose "$@" down --remove-orphans
docker compose pull prometheus grafana
if [ "$#" -gt 0 ]; then docker compose "$@" pull mosquitto influxdb; fi
docker compose "$@" up --build --force-recreate -d

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
echo "Live service logs follow. Ctrl+C stops log viewing; containers stay running."

if command -v open >/dev/null 2>&1; then open "http://localhost:${APP_PORT_VALUE}"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "http://localhost:${APP_PORT_VALUE}"
fi
docker compose "$@" logs --tail=30 -f
