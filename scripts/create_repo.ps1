# Create a new GitHub repository and push the current project
# Requires: git and GitHub CLI (gh) installed and authenticated
param(
    [string]$Name = "modern_python_demo",
    [string]$Visibility = "public",
    [switch]$Push
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "GitHub CLI 'gh' not found. You can still create a remote manually." -ForegroundColor Yellow
    exit 1
}

# Create repo via gh
Write-Host "Creating repository $Name (visibility=$Visibility) on GitHub..."
$createArgs = @('repo', 'create', $Name, "--$Visibility", '--source=.', '--remote=origin', '--push')
if (-not $Push) { $createArgs = $createArgs | Where-Object { $_ -ne '--push' } }
gh @createArgs

Write-Host "Repository creation step finished. If '--push' was not used, push manually: git push -u origin main"