import json
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from google.antigravity import Agent


class CommissioningEvaluation(BaseModel):
    status: str = Field(description="Classification: pass, fail, or warning")
    delay_days: int = Field(description="Number of delay days to inject if fail or warning")
    risk_task_ids: List[int] = Field(description="Task IDs of downstream tasks affected by this delay")
    summary: str = Field(description="Natural language evaluation summary")
    affected_systems: List[str] = Field(description="Systems affected by the issue (e.g., Electrical, Mechanical)")
    test_notes: str = Field(description="Original test notes")


COMMISSIONING_AGENT = Agent(
    model="gemini-2.0-flash",
    response_schema=CommissioningEvaluation,
    system_prompt=(
        "You are a Commissioning Test Evaluation Agent for data centre projects. "
        "Analyze test notes and observations to classify result:\n"
        "- pass: All criteria met, no issues found\n"
        "- fail: Critical failures detected (shutdown, trip, overheat, pressure drop, error, fault) "
        "- typically 5-10 day delay, affects downstream integrated tests\n"
        "- warning: Minor issues found (calibration, adjustment) - typically 1-3 day delay\n\n"
        "For failures, identify affected downstream tasks (typically integrated system tests "
        "like step 20 and final inspection step 22). For warnings, only immediate dependent tasks. "
        "Assign realistic delay days proportional to severity."
    ),
)


COMMISSIONING_STEPS = [
    {"id": 1, "name": "Pre-Commissioning Inspection", "description": "Verify installation completeness", "category": "Electrical"},
    {"id": 2, "name": "MV Switchgear Megger Test", "description": "Insulation resistance test", "category": "Electrical"},
    {"id": 3, "name": "LV Panel Functional Test", "description": "Breaker operation & interlocks", "category": "Electrical"},
    {"id": 4, "name": "Generator No-Load Test", "description": "Start & run without load", "category": "Electrical"},
    {"id": 5, "name": "Generator 4hr Full Load Test", "description": "Full capacity load bank test", "category": "Electrical"},
    {"id": 6, "name": "UPS Battery Discharge Test", "description": "Validate 20min runtime", "category": "Electrical"},
    {"id": 7, "name": "UPS Transfer Time Test", "description": "Break-make transfer <10ms", "category": "Electrical"},
    {"id": 8, "name": "Chiller Performance Test", "description": "COP verification at full load", "category": "Mechanical"},
    {"id": 9, "name": "CRAC/CRAH Air Balance", "description": "Airflow & temperature uniformity", "category": "Mechanical"},
    {"id": 10, "name": "Pump Sequencing Test", "description": "Lead-lag operation", "category": "Mechanical"},
    {"id": 11, "name": "VESDA Sensitivity Test", "description": "Smoke detection sensitivity", "category": "Life Safety"},
    {"id": 12, "name": "Suppression System Discharge Test", "description": "Clean agent discharge", "category": "Life Safety"},
    {"id": 13, "name": "Door Hold Release Test", "description": "Magnetic hold release on alarm", "category": "Life Safety"},
    {"id": 14, "name": "CCTV Camera Coverage Test", "description": "100% coverage verification", "category": "Security"},
    {"id": 15, "name": "Access Control Functionality", "description": "Biometric & card reader test", "category": "Security"},
    {"id": 16, "name": "BMS Sensor Calibration", "description": "Temperature, humidity, pressure", "category": "Controls"},
    {"id": 17, "name": "BMS Alarm Escalation Test", "description": "Alert routing & notifications", "category": "Controls"},
    {"id": 18, "name": "Network Fiber Connectivity Test", "description": "Backbone & patch panel testing", "category": "Network"},
    {"id": 19, "name": "Integrated Power Failover Test", "description": "Black-box full failover", "category": "Integrated"},
    {"id": 20, "name": "Mechanical System Failover", "description": "Chiller, CRAC failover", "category": "Integrated"},
    {"id": 21, "name": "Full System Simulation", "description": "24hr continuous run", "category": "Integrated"},
    {"id": 22, "name": "Final Documentation & Sign-off", "description": "As-built & test reports", "category": "QA"}
]


def evaluate_test_result(test_notes: str) -> Dict[str, Any]:
    prompt = (
        f"Evaluate the following commissioning test notes:\n\n"
        f"{test_notes}\n\n"
        f"Classify as pass/fail/warning. If fail, assign appropriate delay days (5-10) "
        f"and affected downstream task IDs (typically 20, 22 for major failures). "
        f"If warning, assign 1-3 delay days and minimal affected tasks. "
        f"Identify which systems are affected."
    )
    result = COMMISSIONING_AGENT.run(prompt=prompt)
    return result


def get_commissioning_steps() -> List[Dict[str, Any]]:
    return COMMISSIONING_STEPS
