# InfraPulse EPC

**AI Intelligence Layer for Data Centre EPC Project Delivery**

---

## Overview

InfraPulse EPC is an AI-powered project intelligence platform designed to improve the planning, monitoring, and commissioning of data centre EPC (Engineering, Procurement, and Construction) projects. It provides early visibility into project risks by combining schedule analytics, AI-assisted decision support, and commissioning management within a single platform.

Instead of managing scheduling, procurement, weather monitoring, and commissioning as separate processes, InfraPulse EPC brings them together into one unified system, allowing project teams to identify risks earlier, understand their impact on project delivery, and take corrective action before delays escalate.

---

## Key Features

### Predictive Schedule Risk Analysis

The platform continuously monitors project activities and identifies potential delays caused by:

* Equipment and material delivery delays
* Workforce shortages
* Weather disruptions
* Commissioning failures

Each identified risk is analyzed against the project's Critical Path Method (CPM) schedule to determine whether it will affect the final completion date.

---

### AI-Powered Multi-Agent System

InfraPulse EPC uses five specialized AI agents that work together to:

* Monitor project risks
* Analyze schedule impacts
* Recommend mitigation strategies
* Support commissioning engineers
* Generate project insights and reports

This provides project managers with actionable recommendations instead of simple alerts.

---

### Intelligent Commissioning Management

The Commissioning QA Copilot guides engineers through testing procedures by:

* Displaying acceptance criteria
* Recording test results
* Automatically detecting non-conformances
* Generating commissioning documentation
* Tracking corrective actions

When a commissioning test fails, the estimated repair and retest duration is automatically sent to the scheduling engine, where it becomes a live project risk.

---

### Unified Risk Dashboard

The dashboard provides a real-time overview of project health, including:

* Project completion forecast
* Critical path visualization
* Active project risks
* Risk severity levels
* Estimated schedule impacts
* AI-generated mitigation options
* Project performance metrics

This enables project teams to prioritize issues based on their actual effect on project delivery.

---

### Automated Reporting

InfraPulse EPC automatically generates commissioning and project reports that include:

* Test execution records
* Pass and fail summaries
* Non-conformance logs
* Corrective actions
* Schedule impact analysis

These reports simplify documentation and support project handover activities.

---

## Technology Stack

### Backend

* FastAPI
* Python
* Uvicorn
* NetworkX (Critical Path Analysis)
* Pydantic

### Frontend

* React (Vite)
* Tailwind CSS
* Recharts
* Lucide Icons

### AI & Data

* Multi-Agent AI Architecture
* Large Language Models for reasoning and recommendations
* Live Weather Integration (Open-Meteo)

---

## Project Architecture

```
                    +-----------------------+
                    |    React Frontend     |
                    +-----------+-----------+
                                |
                                |
                     REST API (FastAPI)
                                |
          +---------------------+----------------------+
          |                                            |
          |                                            |
+----------------------+                 +-------------------------+
| Schedule Risk Engine |                 | Commissioning QA Copilot|
+----------------------+                 +-------------------------+
          |                                            |
          +---------------------+----------------------+
                                |
                        AI Multi-Agent Layer
                                |
              +-----------------+-----------------+
              |                 |                 |
      Weather Data      Project Analytics    Risk Prediction
```

---

## Quick Start

### Windows

```powershell
.\start.ps1
```

### Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

---

## Manual Installation

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

Open another terminal.

```bash
cd frontend

npm install

npm run dev
```

---

## How It Works

1. The scheduling engine continuously monitors procurement, staffing, weather, and commissioning activities.

2. AI agents evaluate project risks and estimate their impact on the critical path.

3. Commissioning engineers perform equipment testing using the Commissioning QA Copilot.

4. Failed tests automatically generate schedule risks.

5. The scheduling engine recalculates the project timeline in real time.

6. The dashboard updates with revised completion forecasts and mitigation recommendations.

---

## Current Capabilities

* Critical Path Method (CPM) scheduling
* Predictive schedule risk detection
* AI-assisted mitigation planning
* Automated commissioning workflows
* Live weather monitoring
* Multi-agent orchestration
* Interactive project dashboard
* Automated project documentation

---

## Future Enhancements

* Primavera P6 integration
* SAP and ERP connectivity
* Procore integration
* Multi-project portfolio management
* User authentication and role-based access control
* Mobile application for field engineers
* Advanced analytics and forecasting
* Real-time IoT equipment monitoring

---

## Project Goal

InfraPulse EPC aims to transform data centre EPC project management by combining AI, predictive analytics, and intelligent commissioning into a single platform. By providing early warnings, automated workflows, and actionable insights, the platform helps project teams reduce delays, improve coordination, and deliver complex infrastructure projects with greater confidence and efficiency.
