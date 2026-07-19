
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ComplianceCheck:
    parameter: str
    required: str
    submitted: str
    compliant: bool
    standard: str


TIA_942_TIER_III = {
    "battery_runtime_minutes": 20,
    "redundancy": "N+2",
    "ups_efficiency_percent": 94,
    "chiller_n_plus_1": True
}


def check_submittal(submittal_data: Dict[str, Any]) -> Dict[str, Any]:
    checks = []

    checks.append(
        ComplianceCheck(
            parameter="Battery Runtime",
            required="≥20 minutes",
            submitted=f"{submittal_data.get('battery_runtime_minutes', 0)} minutes",
            compliant=submittal_data.get('battery_runtime_minutes', 0) >= TIA_942_TIER_III["battery_runtime_minutes"],
            standard="TIA-942 Tier III"
        )
    )
    checks.append(
        ComplianceCheck(
            parameter="Redundancy",
            required="N+2",
            submitted=submittal_data.get('redundancy', 'N'),
            compliant=submittal_data.get('redundancy', 'N') == TIA_942_TIER_III["redundancy"],
            standard="TIA-942 Tier III"
        )
    )
    checks.append(
        ComplianceCheck(
            parameter="UPS Efficiency",
            required="≥94%",
            submitted=f"{submittal_data.get('ups_efficiency_percent', 0)}%",
            compliant=submittal_data.get('ups_efficiency_percent', 0) >= TIA_942_TIER_III["ups_efficiency_percent"],
            standard="TIA-942 Tier III"
        )
    )
    checks.append(
        ComplianceCheck(
            parameter="Chiller Redundancy",
            required="N+1",
            submitted="Yes" if submittal_data.get('chiller_n_plus_1', False) else "No",
            compliant=submittal_data.get('chiller_n_plus_1', False) == TIA_942_TIER_III["chiller_n_plus_1"],
            standard="TIA-942 Tier III"
        )
    )

    compliant_count = sum(1 for c in checks if c.compliant)
    total_count = len(checks)

    return {
        "submittal_name": submittal_data.get('submittal_name', 'Unknown'),
        "checks": [
            {
                "parameter": c.parameter,
                "required": c.required,
                "submitted": c.submitted,
                "compliant": c.compliant,
                "standard": c.standard
            } for c in checks
        ],
        "overall_compliant": compliant_count == total_count,
        "compliance_score": round((compliant_count / total_count) * 100, 1)
    }

