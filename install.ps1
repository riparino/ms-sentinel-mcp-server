# Microsoft Sentinel MCP Server Installation Script
Write-Host "Setting up Microsoft Sentinel MCP Server..." -ForegroundColor Cyan

# Get script directory for relative paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# MCP Server display name, used in Claude configuration
$mcpDisplayName = "MS Sentinel MCP Server"

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python not found. Please install Python 3.13 or later." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path (Join-Path -Path $scriptDir -ChildPath ".venv"))) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    Set-Location -Path $scriptDir
    python -m venv .venv
}

# Activate virtual environment and install dependencies
Write-Host "Installing dependencies in virtual environment..." -ForegroundColor Yellow
& (Join-Path -Path $scriptDir -ChildPath ".venv\Scripts\python.exe") -m pip install --upgrade pip
& (Join-Path -Path $scriptDir -ChildPath ".venv\Scripts\pip.exe") install -e .

# Create the configuration file
$pythonPath = (Get-Item (Join-Path -Path $scriptDir -ChildPath ".venv\Scripts\python.exe")).FullName
$wrapperPath = (Get-Item (Join-Path -Path $scriptDir -ChildPath "wrapper.py")).FullName

# Run post-installation steps
Write-Host "Running post-installation steps..." -ForegroundColor Yellow
& (Join-Path -Path $scriptDir -ChildPath ".venv\Scripts\python.exe") (Join-Path -Path $scriptDir -ChildPath "post_install.py")

$fallbackConfigPath = Join-Path -Path $scriptDir -ChildPath "claude_desktop_config.json"
$sampleConfigPath = $fallbackConfigPath

# Read environment variables from .env.example
$envFilePath = Join-Path -Path $scriptDir -ChildPath ".env.example"
$envVars = @{}

if (Test-Path $envFilePath) {
    Write-Host "Reading environment variables from .env.example..." -ForegroundColor Yellow
    $envContent = Get-Content -Path $envFilePath -Raw
    $envLines = $envContent -split "`n" | Where-Object { $_ -match '^[A-Za-z]' }
    
    foreach ($line in $envLines) {
        if ($line -match '^([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
            $key = $matches[1]
            $value = $matches[2].Trim()
            $envVars[$key] = $value
        }
    }
}

# Create the configuration object with the exact structure needed
$configObject = @{
    mcpServers = @{
        "$mcpDisplayName" = @{
            command = $pythonPath
            args = @($wrapperPath)
            env = $envVars
        }
    }
}

# Convert to JSON and write to file
try {
    $configJson = $configObject | ConvertTo-Json -Depth 5
    Set-Content -Path $sampleConfigPath -Value $configJson
    Write-Host "Configuration saved to: $sampleConfigPath" -ForegroundColor Green
}
catch {
    Write-Host "Error saving configuration: $_" -ForegroundColor Red
}

# Copy configuration to clipboard
Set-Clipboard -Value $configJson

# Display configuration instructions
Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "`nTo use with your MCP Client (Claude, Cursor, etc.), add the following configuration:" -ForegroundColor Cyan
Write-Host $configJson -ForegroundColor Yellow
Write-Host "`nThis configuration has been saved to: $sampleConfigPath" -ForegroundColor Cyan
Write-Host "`nIt has also been copied to clipboard" -ForegroundColor Cyan