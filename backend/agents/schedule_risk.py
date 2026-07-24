import json
from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from google.antigravity import Agent


class RiskItem(BaseModel):
    task_id: int = Field(description="ID of the affected task")
    task_name: str = Field(description="Name of the affected task")
    risk_type: str = Field(description="Category: Weather Risk, Supply Chain Risk, Resource Risk, Schedule Risk")
    severity: str = Field(description="High, Medium, or Low")
    impact_days: int = Field(description="Estimated delay in days if risk materializes")
    mitigation: str = Field(description="Recommended mitigation action")
    description: str = Field(description="Detailed risk description")


class ScheduleRiskResult(BaseModel):
    total_risks: int = Field(description="Total number of risks identified")
    high_severity: int = Field(description="Count of high severity risks")
    medium_severity: int = Field(description="Count of medium severity risks")
    low_severity: int = Field(description="Count of low severity risks")
    risks: List[RiskItem] = Field(description="List of identified risks")


RISK_AGENT = Agent(
    model="gemini-2.0-flash",
    response_schema=ScheduleRiskResult,
    system_prompt=(
        "You are a Schedule Risk Analysis Agent for data centre EPC projects. "
        "Analyze the project task list and identify:\n"
        "1. Weather risks (monsoon, wind, temperature) for outdoor/civil tasks\n"
        "2. Supply chain risks for tasks with long-lead electrical or mechanical items\n"
        "3. Resource risks for tasks sharing the same resource type\n"
        "4. Schedule risks on critical path tasks with tight dependencies\n"
        "Consider Pune, India location and typical monsoon season (June-September). "
        "Assign severity based on critical path impact. "
        "Provide concrete mitigation suggestions."
    ),
)


def _serialize_tasks(tasks):
    def default(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    return json.dumps(tasks, indent=2, default=default)


def predict_risks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    tasks_text = _serialize_tasks(tasks)
    prompt = (
        f"Analyze the following project tasks for schedule, weather, supply chain, "
        f"and resource risks. The project is located in Pune, India. "
        f"Consider monsoon season impacts on civil and outdoor tasks.\n\n{tasks_text}"
    )
    result = RISK_AGENT.run(prompt=prompt)
    return result
