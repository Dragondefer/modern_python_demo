param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

# Resolve project root relative to this script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Root = Resolve-Path (Join-Path $ScriptDir "..")

# Paths
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$Requirements = Join-Path $Root "requirements.txt"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv (Join-Path $Root ".venv")
}

$py = (Resolve-Path $VenvPython).Path
& $py -m pip install --upgrade pip
if (Test-Path $Requirements) {
    & $py -m pip install -r $Requirements
} else {
    Write-Host "No requirements.txt found at $Requirements - continuing without installing extras" -ForegroundColor Yellow
}

# Run the demo using the venv python
& $py -m modern_python_demo @Args
