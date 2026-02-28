# Architectural Image Generator Launcher
# This script helps you generate professional architectural renderings

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "   🏗️  ARCHITECTURAL IMAGE GENERATOR" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Find the most recent design JSON file
$jsonFiles = Get-ChildItem -Path "." -Filter "design_data_*.json" | Sort-Object LastWriteTime -Descending

if ($jsonFiles.Count -eq 0) {
    Write-Host "❌ ERROR: No design data files found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please generate a design first by:" -ForegroundColor Yellow
    Write-Host "  1. Opening design_interface_v2.html" -ForegroundColor White
    Write-Host "  2. Filling in the form" -ForegroundColor White
    Write-Host "  3. Clicking 'Generate Complete Design'" -ForegroundColor White
    Write-Host "  4. Clicking '🏗️ Generate Architectural Images'" -ForegroundColor White
    Write-Host ""
    pause
    exit
}

$latestFile = $jsonFiles[0].Name
Write-Host "📁 Found design file: $latestFile" -ForegroundColor Green
Write-Host ""

# Check if multiple files exist
if ($jsonFiles.Count -gt 1) {
    Write-Host "Multiple design files found. Using the most recent one." -ForegroundColor Yellow
    Write-Host "Other files:" -ForegroundColor Gray
    for ($i = 1; $i -lt [Math]::Min($jsonFiles.Count, 5); $i++) {
        Write-Host "  - $($jsonFiles[$i].Name)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& ../.venv/Scripts/Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Make sure .venv exists in the parent directory" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Check if required packages are installed
Write-Host "📦 Checking required packages..." -ForegroundColor Cyan
$requiredPackages = @("matplotlib", "numpy", "pillow")
$missingPackages = @()

foreach ($pkg in $requiredPackages) {
    $installed = & python -c "import $pkg" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $pkg
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "⚠️  Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "Installing missing packages..." -ForegroundColor Cyan
    pip install $missingPackages
    Write-Host ""
}

# Generate images
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🎨 GENERATING ARCHITECTURAL RENDERINGS..." -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

python generate_architectural_images.py $latestFile

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "   ✅ SUCCESS! All images generated" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Check the 'exports/design_*/' folder to view your images" -ForegroundColor Cyan
    Write-Host ""
    
    # Attempt to open the output directory
    $exportDirs = Get-ChildItem -Path "exports" -Directory | Sort-Object LastWriteTime -Descending
    if ($exportDirs.Count -gt 0) {
        $latestExport = $exportDirs[0].FullName
        Write-Host "Opening output directory..." -ForegroundColor Cyan
        Start-Process explorer.exe $latestExport
    }
} else {
    Write-Host ""
    Write-Host "❌ Error occurred during image generation" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
