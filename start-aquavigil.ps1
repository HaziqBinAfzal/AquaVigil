$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Read-EnvFile {
    param([string]$Path)
    $values = @{}
    if (Test-Path $Path) {
        foreach ($line in Get-Content $Path) {
            $trimmed = $line.Trim()
            if ($trimmed -and -not $trimmed.StartsWith("#") -and $trimmed.Contains("=")) {
                $parts = $trimmed.Split("=", 2)
                $values[$parts[0].Trim()] = $parts[1].Trim()
            }
        }
    }
    return $values
}

function Get-AvailablePort {
    param([int]$PreferredPort, [string]$Service)
    $candidate = $PreferredPort
    while (Get-NetTCPConnection -LocalPort $candidate -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1) {
        $candidate++
        if ($candidate -gt ($PreferredPort + 50)) { throw "No available port found for $Service near $PreferredPort." }
    }
    if ($candidate -ne $PreferredPort) { Write-Host "$Service port $PreferredPort is busy; using $candidate automatically." -ForegroundColor Yellow }
    return $candidate
}

function Set-EnvValue {
    param([string]$Path, [string]$Name, [string]$Value)
    $lines = @(Get-Content $Path)
    $found = $false
    $updated = foreach ($line in $lines) {
        if ($line -match "^$([regex]::Escape($Name))=") { $found = $true; "$Name=$Value" } else { $line }
    }
    if (-not $found) { $updated += "$Name=$Value" }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines((Resolve-Path $Path), [string[]]$updated, $utf8NoBom)
}

$Host.UI.RawUI.WindowTitle = "AquaVigil | Water Security Operations"
Clear-Host
Write-Host "  ==============================================================" -ForegroundColor DarkCyan
Write-Host "    A Q U A V I G I L        ~ ~ ~   [ SHIELD ]" -ForegroundColor Cyan
Write-Host "    WATER SECURITY  /  DESALINATION  /  EVIDENCE MONITORING" -ForegroundColor White
Write-Host "  ==============================================================" -ForegroundColor DarkCyan
Write-Host "    READ-ONLY DEMONSTRATION  |  No plant control commands" -ForegroundColor Yellow
Write-Host ""
function Stage([int]$Number, [string]$Label) {
    Write-Host ("  [{0}/6] {1}" -f $Number, $Label) -ForegroundColor Cyan
}

Stage 1 "Checking Docker engine"

$dockerDesktop = Join-Path $env:ProgramFiles "Docker\Docker\Docker Desktop.exe"
$dockerCliDir = Join-Path $env:ProgramFiles "Docker\Docker\resources\bin"
if (-not (Get-Command docker -ErrorAction SilentlyContinue) -and (Test-Path $dockerCliDir)) {
    $env:Path = "$dockerCliDir;$env:Path"
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw "Docker Desktop is not installed. Install it once, then double-click OPEN-AQUAVIGIL.vbs." }
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    if (-not (Test-Path $dockerDesktop)) { throw "Docker Desktop could not be found." }
    Write-Host "Starting Docker Desktop automatically..." -ForegroundColor Cyan
    Start-Process $dockerDesktop
    $dockerDeadline = (Get-Date).AddMinutes(3)
    do {
        Start-Sleep -Seconds 3
        docker info *> $null
    } while ($LASTEXITCODE -ne 0 -and (Get-Date) -lt $dockerDeadline)
    if ($LASTEXITCODE -ne 0) { throw "Docker Desktop did not become ready within three minutes." }
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example." -ForegroundColor Green
}

Stage 2 "Reading settings and finding available ports"
$config = Read-EnvFile ".env"
# Upgrade earlier installations that still contain RESET_ON_START=1.
# Intentional clearing remains a separate, explicit maintenance action.
if ($config["AQUAVIGIL_RESET_ON_START"] -ne "0") {
    Set-EnvValue ".env" "AQUAVIGIL_RESET_ON_START" "0"
    Write-Host "  Analysis history preservation enabled for this installation." -ForegroundColor Green
}
$appPort = if ($config["APP_PORT"]) { [int]$config["APP_PORT"] } else { 8000 }
$prometheusPort = if ($config["PROMETHEUS_PORT"]) { [int]$config["PROMETHEUS_PORT"] } else { 9090 }
$grafanaPort = if ($config["GRAFANA_PORT"]) { [int]$config["GRAFANA_PORT"] } else { 3000 }
$composeOptions = @()
if ($config["MQTT_ENABLED"] -eq "1") {
    $composeOptions = @("--profile", "simulator")
    Write-Host "  Local synthetic MQTT and InfluxDB simulation enabled." -ForegroundColor Yellow
}

# Preserve the named volume and every stored analysis across restarts.
docker compose @composeOptions down --remove-orphans *> $null
$appPort = Get-AvailablePort $appPort "AquaVigil"
$prometheusPort = Get-AvailablePort $prometheusPort "Prometheus"
$grafanaPort = Get-AvailablePort $grafanaPort "Grafana"
Set-EnvValue ".env" "APP_PORT" $appPort
Set-EnvValue ".env" "PROMETHEUS_PORT" $prometheusPort
Set-EnvValue ".env" "GRAFANA_PORT" $grafanaPort

Stage 3 "Checking monitoring images"
docker image inspect prom/prometheus:v3.5.0 *> $null
if ($LASTEXITCODE -ne 0) { docker compose pull prometheus; if ($LASTEXITCODE -ne 0) { throw "Prometheus image could not be downloaded." } }
docker image inspect grafana/grafana:12.1.1 *> $null
if ($LASTEXITCODE -ne 0) { docker compose pull grafana; if ($LASTEXITCODE -ne 0) { throw "Grafana image could not be downloaded." } }
if ($composeOptions.Count -gt 0) {
    docker compose @composeOptions pull mosquitto influxdb
    if ($LASTEXITCODE -ne 0) { throw "Optional simulation images could not be downloaded." }
}

Stage 4 "Building application and starting services"
docker compose @composeOptions up --build --force-recreate -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose could not start AquaVigil." }

$appUrl = "http://localhost:$appPort"
$deadline = (Get-Date).AddMinutes(2)
$ready = $false
Stage 5 "Waiting for application health check"
Write-Host "  AquaVigil" -NoNewline
while ((Get-Date) -lt $deadline) {
    try {
        $health = Invoke-RestMethod -Uri "$appUrl/health" -TimeoutSec 3
        if ($health.status -eq "ok") { $ready = $true; break }
    } catch {}
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 2
}
Write-Host ""

if (-not $ready) {
    docker compose ps
    throw "AquaVigil did not become healthy within two minutes. Run docker compose logs aquavigil."
}

Stage 6 "Services ready"
docker compose @composeOptions ps
Write-Host "  APPLICATION   $appUrl" -ForegroundColor Green
Write-Host "  PROMETHEUS    http://localhost:$prometheusPort" -ForegroundColor White
Write-Host "  GRAFANA       http://localhost:$grafanaPort" -ForegroundColor White
Write-Host ""
Start-Process $appUrl
Write-Host "  LIVE APPLICATION LOGS  |  Press Ctrl+C to stop viewing logs; services keep running." -ForegroundColor Cyan
Write-Host "  Stop services using STOP-AQUAVIGIL.cmd when finished." -ForegroundColor DarkCyan
docker compose @composeOptions logs --tail=30 -f
