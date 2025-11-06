param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

# Ensure venv exists and use its python to run the demo. This script installs
# requirements automatically if needed so you don't have to activate the venv.
try {
    $venvPy = Resolve-Path "..\.venv\Scripts\python.exe" -ErrorAction Stop
} catch {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
    $venvPy = Resolve-Path "..\.venv\Scripts\python.exe"
}

$py = $venvPy.Path
& $py -m pip install --upgrade pip
& $py -m pip install -r "..\requirements.txt"

# Run the demo using the venv python
& $py -m modern_python_demo @Args
