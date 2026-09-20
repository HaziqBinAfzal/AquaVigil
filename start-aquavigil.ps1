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

Write-Host ""
Write-Host "AquaVigil Docker Launcher" -ForegroundColor Cyan
Write-Host "Smart Water and Desalination Security Platform" -ForegroundColor DarkCyan
Write-Host ""

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

$config = Read-EnvFile ".env"
$appPort = if ($config["APP_PORT"]) { [int]$config["APP_PORT"] } else { 8000 }
$prometheusPort = if ($config["PROMETHEUS_PORT"]) { [int]$config["PROMETHEUS_PORT"] } else { 9090 }
$grafanaPort = if ($config["GRAFANA_PORT"]) { [int]$config["GRAFANA_PORT"] } else { 3000 }

Write-Host "Clearing the previous demonstration session..." -ForegroundColor Cyan
docker compose down --remove-orphans --volumes *> $null
$appPort = Get-AvailablePort $appPort "AquaVigil"
$prometheusPort = Get-AvailablePort $prometheusPort "Prometheus"
$grafanaPort = Get-AvailablePort $grafanaPort "Grafana"
Set-EnvValue ".env" "APP_PORT" $appPort
Set-EnvValue ".env" "PROMETHEUS_PORT" $prometheusPort
Set-EnvValue ".env" "GRAFANA_PORT" $grafanaPort

Write-Host "Pulling required monitoring images..." -ForegroundColor Cyan
docker compose pull prometheus grafana
if ($LASTEXITCODE -ne 0) { throw "Docker could not download the monitoring images. Check the internet connection and retry." }

Write-Host "Building and starting AquaVigil..." -ForegroundColor Cyan
docker compose up --build --force-recreate -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose could not start AquaVigil." }

$appUrl = "http://localhost:$appPort"
$deadline = (Get-Date).AddMinutes(2)
$ready = $false
Write-Host "Waiting for the application health check" -NoNewline
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

Write-Host "AquaVigil is ready." -ForegroundColor Green
Write-Host "Application: $appUrl" -ForegroundColor White
Write-Host "Prometheus: http://localhost:$prometheusPort" -ForegroundColor White
Write-Host "Grafana: http://localhost:$grafanaPort  (admin / aquavigil)" -ForegroundColor White
Write-Host ""
Start-Process $appUrl
