# LLM Council - Start script (Windows PowerShell)

Write-Host ""
Write-Host "Starting LLM Council..." -ForegroundColor Cyan
Write-Host ""

# Start backend in a new window
Write-Host "Starting backend on http://localhost:8001..." -ForegroundColor Yellow
$backend = Start-Process -FilePath "cmd.exe" -ArgumentList "/c python -m backend.main" -WorkingDirectory $PSScriptRoot -PassThru

# Wait for backend to initialize
Start-Sleep -Seconds 2

# Start frontend in a new window
Write-Host "Starting frontend on http://localhost:5173..." -ForegroundColor Yellow
$frontend = Start-Process -FilePath "cmd.exe" -ArgumentList "/c npx vite --host" -WorkingDirectory "$PSScriptRoot\frontend" -PassThru

Write-Host ""
Write-Host "LLM Council is running!" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8001" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to stop both servers..." -ForegroundColor Gray

# Wait for user to press Enter
Read-Host

# Stop both processes
Write-Host "Stopping servers..." -ForegroundColor Yellow
if ($backend -and !$backend.HasExited) { Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue }
if ($frontend -and !$frontend.HasExited) { Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue }
Write-Host "Servers stopped." -ForegroundColor Green
