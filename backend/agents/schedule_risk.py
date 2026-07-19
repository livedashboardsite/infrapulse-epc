
from typing import List, Dict, Any
from datetime import datetime, timedelta


def predict_risks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    risks = []

    for task in tasks:
        if task["is_critical"]:
            if "Excavation" in task["name"]:
                risks.append({
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "risk_type": "Weather Risk",
                    "mitigation": "Accelerate foundation work before monsoon",
                    "impact_days": 10,
                    "severity": "High"
                })
            if "Commissioning" in task["name"]:
                risks.append({
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "risk_type": "Supply Chain Risk",
                    "mitigation": "Verify long lead items 60 days prior",
                    "impact_days": 8,
                    "severity": "High"
                })
        if "Outdoor" in task["name"] or "Erection" in task["name"]:
            risks.append({
                "task_id": task["id"],
                "task_name": task["name"],
                "risk_type": "Wind Risk",
                "mitigation": "Monitor wind speed; stop crane ops >35 km/h",
                "impact_days": 5,
                "severity": "Medium"
            })

    return {
        "total_risks": len(risks),
        "high_severity": sum(1 for r in risks if r["severity"] == "High"),
        "medium_severity": sum(1 for r in risks if r["severity"] == "Medium"),
        "low_severity": sum(1 for r in risks if r["severity"] == "Low"),
        "risks": risks
    }

