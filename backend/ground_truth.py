
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any

@dataclass
class Task:
    id: int
    name: str
    description: str
    duration_days: int
    dependencies: List[int]
    start_date: datetime
    end_date: datetime
    is_critical: bool
    resource_type: str
    location: str


def get_ground_truth_tasks() -> List[Dict[str, Any]]:
    base_date = datetime(2024, 1, 1)

    tasks = [
        {"id": 1, "name": "Site Survey & Permits", "description": "Topographical survey & regulatory approvals", "duration_days": 30, "dependencies": [], "start_date": base_date, "end_date": base_date + timedelta(days=30), "is_critical": True, "resource_type": "Engineering", "location": "Pune, India"},
        {"id": 2, "name": "Site Clearing & Grubbing", "description": "Remove vegetation & prepare building pad", "duration_days": 15, "dependencies": [1], "start_date": base_date + timedelta(days=30), "end_date": base_date + timedelta(days=45), "is_critical": True, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 3, "name": "Excavation & Foundation", "description": "Deep foundation for data hall & utility blocks", "duration_days": 60, "dependencies": [2], "start_date": base_date + timedelta(days=45), "end_date": base_date + timedelta(days=105), "is_critical": True, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 4, "name": "Structural Steel Erection", "description": "Erect steel frame for data halls", "duration_days": 45, "dependencies": [3], "start_date": base_date + timedelta(days=105), "end_date": base_date + timedelta(days=150), "is_critical": True, "resource_type": "Structural", "location": "Pune, India"},
        {"id": 5, "name": "Roof & Envelope", "description": "Waterproof roof & insulated facade", "duration_days": 30, "dependencies": [4], "start_date": base_date + timedelta(days=150), "end_date": base_date + timedelta(days=180), "is_critical": True, "resource_type": "Structural", "location": "Pune, India"},
        {"id": 6, "name": "Electrical Room Infrastructure", "description": "Install LV, MV switchgear & bus ducts", "duration_days": 40, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=220), "is_critical": True, "resource_type": "Electrical", "location": "Pune, India"},
        {"id": 7, "name": "UPS System Installation", "description": "N+1 UPS modules & battery strings", "duration_days": 35, "dependencies": [6], "start_date": base_date + timedelta(days=220), "end_date": base_date + timedelta(days=255), "is_critical": True, "resource_type": "Electrical", "location": "Pune, India"},
        {"id": 8, "name": "Generator Delivery & Installation", "description": "2MW diesel generators, fuel tanks", "duration_days": 50, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=230), "is_critical": True, "resource_type": "Electrical", "location": "Pune, India"},
        {"id": 9, "name": "Mechanical Room Infrastructure", "description": "Chiller plant, pumps, pipework", "duration_days": 45, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=225), "is_critical": False, "resource_type": "Mechanical", "location": "Pune, India"},
        {"id": 10, "name": "CRAC/CRAH Installation", "description": "Computer room air handlers", "duration_days": 30, "dependencies": [9], "start_date": base_date + timedelta(days=225), "end_date": base_date + timedelta(days=255), "is_critical": False, "resource_type": "Mechanical", "location": "Pune, India"},
        {"id": 11, "name": "Raised Access Floor", "description": "600mm raised floor, grommets", "duration_days": 20, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=200), "is_critical": False, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 12, "name": "Cabling Infrastructure", "description": "Fiber backbone, copper patch panels", "duration_days": 40, "dependencies": [11], "start_date": base_date + timedelta(days=200), "end_date": base_date + timedelta(days=240), "is_critical": False, "resource_type": "Network", "location": "Pune, India"},
        {"id": 13, "name": "Fire Suppression System", "description": "VESDA, clean agent suppression", "duration_days": 30, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=210), "is_critical": True, "resource_type": "Life Safety", "location": "Pune, India"},
        {"id": 14, "name": "Security & Access Control", "description": "CCTV, biometrics, mantraps", "duration_days": 25, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=205), "is_critical": False, "resource_type": "Security", "location": "Pune, India"},
        {"id": 15, "name": "Building Management System", "description": "BMS sensors, controllers, dashboards", "duration_days": 35, "dependencies": [13,14], "start_date": base_date + timedelta(days=210), "end_date": base_date + timedelta(days=245), "is_critical": False, "resource_type": "Controls", "location": "Pune, India"},
        {"id": 16, "name": "Generator Testing Prep", "description": "Load bank connection, fuel fill", "duration_days": 15, "dependencies": [8], "start_date": base_date + timedelta(days=230), "end_date": base_date + timedelta(days=245), "is_critical": True, "resource_type": "Commissioning", "location": "Pune, India"},
        {"id": 17, "name": "UPS Commissioning", "description": "Battery discharge test, transfer time", "duration_days": 20, "dependencies": [7,16], "start_date": base_date + timedelta(days=255), "end_date": base_date + timedelta(days=275), "is_critical": True, "resource_type": "Commissioning", "location": "Pune, India"},
        {"id": 18, "name": "Mechanical Commissioning", "description": "Chiller sequencing, air balancing", "duration_days": 25, "dependencies": [10,15], "start_date": base_date + timedelta(days=255), "end_date": base_date + timedelta(days=280), "is_critical": False, "resource_type": "Commissioning", "location": "Pune, India"},
        {"id": 19, "name": "Fire System Commissioning", "description": "Smoke test, suppression discharge", "duration_days": 15, "dependencies": [15,13], "start_date": base_date + timedelta(days=245), "end_date": base_date + timedelta(days=260), "is_critical": True, "resource_type": "Commissioning", "location": "Pune, India"},
        {"id": 20, "name": "Integrated Systems Test", "description": "Full black-box failover simulation", "duration_days": 30, "dependencies": [17,18,19], "start_date": base_date + timedelta(days=280), "end_date": base_date + timedelta(days=310), "is_critical": True, "resource_type": "Commissioning", "location": "Pune, India"},
        {"id": 21, "name": "Rack & Stack Preparation", "description": "Server racks, PDU installation", "duration_days": 20, "dependencies": [12], "start_date": base_date + timedelta(days=240), "end_date": base_date + timedelta(days=260), "is_critical": False, "resource_type": "IT", "location": "Pune, India"},
        {"id": 22, "name": "Final Inspection & Audit", "description": "Uptime Institute Tier III audit", "duration_days": 20, "dependencies": [20], "start_date": base_date + timedelta(days=310), "end_date": base_date + timedelta(days=330), "is_critical": True, "resource_type": "QA", "location": "Pune, India"},
        {"id": 23, "name": "Utility Power Connection", "description": "Grid connection & metering", "duration_days": 45, "dependencies": [1], "start_date": base_date + timedelta(days=30), "end_date": base_date + timedelta(days=75), "is_critical": True, "resource_type": "Utility", "location": "Pune, India"},
        {"id": 24, "name": "Water Supply & Drainage", "description": "Potable water & stormwater system", "duration_days": 30, "dependencies": [2], "start_date": base_date + timedelta(days=45), "end_date": base_date + timedelta(days=75), "is_critical": False, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 25, "name": "External Landscaping", "description": "Site hardscaping & green buffer", "duration_days": 40, "dependencies": [5], "start_date": base_date + timedelta(days=180), "end_date": base_date + timedelta(days=220), "is_critical": False, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 26, "name": "Security Fencing & Gates", "description": "Perimeter fence, vehicle access control", "duration_days": 25, "dependencies": [2], "start_date": base_date + timedelta(days=45), "end_date": base_date + timedelta(days=70), "is_critical": False, "resource_type": "Security", "location": "Pune, India"},
        {"id": 27, "name": "Parking & Access Roads", "description": "Truck access & staff parking", "duration_days": 35, "dependencies": [26], "start_date": base_date + timedelta(days=70), "end_date": base_date + timedelta(days=105), "is_critical": False, "resource_type": "Civil", "location": "Pune, India"},
        {"id": 28, "name": "Telecom Fiber Entry", "description": "Diverse fiber paths from carriers", "duration_days": 50, "dependencies": [1], "start_date": base_date + timedelta(days=30), "end_date": base_date + timedelta(days=80), "is_critical": True, "resource_type": "Network", "location": "Pune, India"},
        {"id": 29, "name": "Staff Training & Orientation", "description": "Operator training on all systems", "duration_days": 20, "dependencies": [20], "start_date": base_date + timedelta(days=310), "end_date": base_date + timedelta(days=330), "is_critical": False, "resource_type": "Training", "location": "Pune, India"},
        {"id": 30, "name": "Substantial Completion", "description": "Project handover & acceptance", "duration_days": 5, "dependencies": [22,29], "start_date": base_date + timedelta(days=330), "end_date": base_date + timedelta(days=335), "is_critical": True, "resource_type": "QA", "location": "Pune, India"}
    ]
    
    return tasks


def get_benchmark_metrics() -> Dict[str, Any]:
    return {
        "days_delay_warning_lead_time": 18,
        "test_automation_coverage_percent": 100,
        "spec_compliance_accuracy_percent": 95,
        "hours_saved_per_week": 42
    }

