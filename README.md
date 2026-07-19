# InfraPulse EPC
AI Intelligence Layer for Data Centre EPC Project Delivery

## Quick Start

### Windows (PowerShell)
```powershell
.\start.ps1
```

### Unix/Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

Or start manually:

1. **Start Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

2. **Start Frontend (in another terminal):
```bash
cd frontend
npm install
npm run dev
```

## Features
- Multi-agent orchestration (5 specialized agents)
- Liquid glass UI with dark/light mode
- Live weather integration (Open-Meteo)
- CPM schedule engine (NetworkX)
- Auto-integrated commissioning loop

## Tech Stack
- Backend: FastAPI, Uvicorn, NetworkX, Pydantic
- Frontend: React (Vite), Tailwind CSS, Recharts, Lucide
