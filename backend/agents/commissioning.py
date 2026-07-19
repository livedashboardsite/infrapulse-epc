
from typing import List, Dict, Any


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
    test_notes_lower = test_notes.lower()

    failure_keywords = ["shut down", "failed", "trip", "overheat", "pressure drop", "error", "fault"]
    warning_keywords = ["warning", "minor issue", "adjustment", "calibrate"]

    status = "pass"
    delay_days = 0
    risk_task_ids = []
    summary = ""

    if any(keyword in test_notes_lower for keyword in failure_keywords):
        status = "fail"
        delay_days = 7
        risk_task_ids = [20, 22]  # Tasks that depend on commissioning
        summary = "Critical failure detected: Automatic 7-day delay injected; project end date recalculated."
    elif any(keyword in test_notes_lower for keyword in warning_keywords):
        status = "warning"
        delay_days = 2
        risk_task_ids = [20]
        summary = "Minor issue detected: 2-day buffer recommended."
    else:
        status = "pass"
        summary = "Test passed successfully."

    return {
        "status": status,
        "delay_days": delay_days,
        "risk_task_ids": risk_task_ids,
        "summary": summary,
        "test_notes": test_notes
    }


def get_commissioning_steps() -> List[Dict[str, Any]]:
    return COMMISSIONING_STEPS

