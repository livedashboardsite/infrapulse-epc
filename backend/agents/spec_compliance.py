import json
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from google.antigravity import Agent, Document


class ComplianceCheck(BaseModel):
    parameter: str = Field(description="Name of the parameter being checked")
    required: str = Field(description="Required value per standard")
    submitted: str = Field(description="Value submitted for review")
    compliant: bool = Field(description="Whether the submission meets the requirement")
    standard: str = Field(description="Standard reference (e.g., TIA-942)")


class SpecComplianceResult(BaseModel):
    submittal_name: str = Field(description="Name of the submittal reviewed")
    checks: List[ComplianceCheck] = Field(description="List of compliance checks performed")
    overall_compliant: bool = Field(description="True if all checks pass")
    compliance_score: float = Field(description="Percentage of checks that passed")
    summary: str = Field(description="Natural language summary of findings")


COMPLIANCE_AGENT = Agent(
    model="gemini-2.0-flash",
    response_schema=SpecComplianceResult,
    system_prompt=(
        "You are a TIA-942 and Uptime Institute compliance verification agent for data centre projects. "
        "Analyze submittal data against Tier III requirements:\n"
        "- Battery Runtime: minimum 20 minutes\n"
        "- Redundancy: N+2 required for Tier III\n"
        "- UPS Efficiency: minimum 94%\n"
        "- Chiller Redundancy: N+1 minimum\n"
        "Return structured compliance results."
    ),
)


def check_submittal(submittal_data: dict[str, Any]) -> dict[str, Any]:
    submittal_text = json.dumps(submittal_data, indent=2)
    prompt = (
        f"Review the following submittal against TIA-942 Tier III standards:\n\n"
        f"{submittal_text}\n\n"
        f"Evaluate battery runtime (≥20min), redundancy (N+2), UPS efficiency (≥94%), "
        f"and chiller N+1 redundancy. Provide a compliance score and summary."
    )
    result = COMPLIANCE_AGENT.run(prompt=prompt)
    return result


def check_submittal_document(document: Document) -> dict[str, Any]:
    prompt = (
        "Review the uploaded submittal document against TIA-942 Tier III standards. "
        "Extract the submittal name, evaluate each parameter against requirements "
        "(battery runtime ≥20min, redundancy N+2, UPS efficiency ≥94%, chiller N+1), "
        "and return a structured compliance report."
    )
    result = COMPLIANCE_AGENT.run(prompt=prompt, document=document)
    return result
