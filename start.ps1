# Start InfraPulse EPC Backend and Frontend on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "InfraPulse EPC - Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nStarting Backend (FastAPI on http://localhost:8000..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m pip install -r requirements.txt; python -m uvicorn main:app --reload"

Start-Sleep -Seconds 3

Write-Host "`nStarting Frontend (Vite on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm install; npm run dev"

Write-Host "`nApplication started successfully!" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor Magenta
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
