import os
import json
from typing import Any, Optional, Type
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Document:
    def __init__(self, content: bytes | str, mime_type: str = "text/plain"):
        self.content = content
        self.mime_type = mime_type

    @classmethod
    def from_text(cls, text: str):
        return cls(content=text, mime_type="text/plain")

    @classmethod
    def from_file(cls, filepath: str):
        with open(filepath, "rb") as f:
            content = f.read()
        ext = filepath.split(".")[-1].lower()
        mime_map = {"pdf": "application/pdf", "txt": "text/plain", "json": "application/json"}
        return cls(content=content, mime_type=mime_map.get(ext, "application/octet-stream"))


def _construct_mock_response(schema: Type[BaseModel], prompt: str) -> dict:
    schema_name = schema.__name__
    prompt_lower = prompt.lower()

    if "SpecComplianceResult" in schema_name or "compliance" in prompt_lower:
        has_failure = any(kw in prompt_lower for kw in ["10 min", "n", "85%", "false", "fail"])
        checks = [
            {"parameter": "Battery Runtime", "required": "≥20 minutes", "submitted": "22 minutes", "compliant": True, "standard": "TIA-942 Tier III"},
            {"parameter": "Redundancy", "required": "N+2", "submitted": "N+2", "compliant": True, "standard": "TIA-942 Tier III"},
            {"parameter": "UPS Efficiency", "required": "≥94%", "submitted": "94.5%", "compliant": True, "standard": "TIA-942 Tier III"},
            {"parameter": "Chiller Redundancy", "required": "N+1", "submitted": "Yes", "compliant": True, "standard": "TIA-942 Tier III"},
        ]
        if has_failure:
            checks[0]["compliant"] = False
            checks[0]["submitted"] = "10 minutes"
            checks[1]["compliant"] = False
            checks[1]["submitted"] = "N"
            checks[2]["compliant"] = False
            checks[2]["submitted"] = "85%"

        compliant_count = sum(1 for c in checks if c["compliant"])
        return {
            "submittal_name": "UPS-01 Submittal",
            "checks": checks,
            "overall_compliant": compliant_count == len(checks),
            "compliance_score": round((compliant_count / len(checks)) * 100, 1),
            "summary": "Mock compliance analysis complete."
        }

    if "ScheduleRiskResult" in schema_name or "risk" in prompt_lower:
        return {
            "total_risks": 3,
            "high_severity": 2,
            "medium_severity": 1,
            "low_severity": 0,
            "risks": [
                {"task_id": 3, "task_name": "Excavation & Foundation", "risk_type": "Weather Risk", "severity": "High", "impact_days": 10, "mitigation": "Accelerate foundation work before monsoon", "description": "Monsoon season delay risk for excavation in Pune"},
                {"task_id": 8, "task_name": "Generator Delivery & Installation", "risk_type": "Supply Chain Risk", "severity": "High", "impact_days": 8, "mitigation": "Verify long lead items 60 days prior", "description": "Long-lead generator delivery risk"},
                {"task_id": 4, "task_name": "Structural Steel Erection", "risk_type": "Weather Risk", "severity": "Medium", "impact_days": 5, "mitigation": "Monitor wind speed; stop crane ops >35 km/h", "description": "Wind risk for outdoor steel erection"},
            ]
        }

    if "CommissioningEvaluation" in schema_name or "commission" in prompt_lower:
        is_fail = any(kw in prompt_lower for kw in ["shut down", "failed", "trip", "overheat", "fault", "error"])
        is_warning = any(kw in prompt_lower for kw in ["warning", "minor", "calibration", "adjustment"])
        if is_fail:
            return {"status": "fail", "delay_days": 7, "risk_task_ids": [20, 22], "summary": "Critical failure detected: 7-day delay injected downstream.", "affected_systems": ["Electrical"], "test_notes": prompt}
        if is_warning:
            return {"status": "warning", "delay_days": 2, "risk_task_ids": [20], "summary": "Minor issue: 2-day buffer recommended.", "affected_systems": ["Controls"], "test_notes": prompt}
        return {"status": "pass", "delay_days": 0, "risk_task_ids": [], "summary": "Test passed successfully.", "affected_systems": [], "test_notes": prompt}

    return schema().model_dump()


class Agent:
    def __init__(
        self,
        model: str = "meta/llama-3.1-70b-instruct",
        tools: Optional[list] = None,
        response_schema: Optional[Type[BaseModel]] = None,
        system_prompt: Optional[str] = None,
    ):
        self.model = model
        self.tools = tools or []
        self.response_schema = response_schema
        self.system_prompt = system_prompt
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self._use_nvidia = bool(self.nvidia_api_key) and self.nvidia_api_key != "your_nvidia_api_key_here"
        self._use_gemini = bool(self.gemini_api_key) and self.gemini_api_key != "your_gemini_api_key_here"
        self._use_real = self._use_nvidia or self._use_gemini

    def run(
        self,
        prompt: str,
        document: Optional[Document] = None,
        **kwargs,
    ) -> Any:
        if self._use_real:
            return self._run_real(prompt, document, **kwargs)
        return self._run_mock(prompt, document, **kwargs)

    def _run_real(self, prompt: str, document: Optional[Document] = None, **kwargs) -> Any:
        if self._use_nvidia:
            return self._run_nvidia(prompt, document, **kwargs)
        return self._run_gemini(prompt, document, **kwargs)

    def _run_nvidia(self, prompt: str, document: Optional[Document] = None, **kwargs) -> Any:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=self.nvidia_api_key
            )
            nim_model = self.model
            if nim_model.startswith("gemini-"):
                nim_model = "meta/llama-3.1-70b-instruct"

            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})

            content_text = prompt
            if document:
                doc_str = document.content.decode('utf-8', errors='ignore') if isinstance(document.content, bytes) else str(document.content)
                content_text += f"\n\nUploaded Document Content:\n{doc_str}"

            if self.response_schema:
                schema_json = json.dumps(self.response_schema.model_json_schema(), indent=2)
                content_text += f"\n\nIMPORTANT: Return ONLY a valid JSON object strictly adhering to this JSON Schema:\n{schema_json}"

            messages.append({"role": "user", "content": content_text})

            completion = client.chat.completions.create(
                model=nim_model,
                messages=messages,
                temperature=0.2,
                top_p=0.7,
            )

            res_text = completion.choices[0].message.content or ""
            if self.response_schema:
                clean_json = res_text.strip()
                if clean_json.startswith("```"):
                    clean_json = clean_json.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                return json.loads(clean_json)
            return res_text
        except Exception as e:
            raise RuntimeError(f"NVIDIA NIM model error: {e}")

    def _run_gemini(self, prompt: str, document: Optional[Document] = None, **kwargs) -> Any:
        try:
            from google import genai

            client = genai.Client(api_key=self.gemini_api_key)
            contents = []
            if document:
                contents.append({
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": document.mime_type, "data": document.content if isinstance(document.content, bytes) else document.content.encode()}}
                    ]
                })
            else:
                contents.append({"role": "user", "parts": [{"text": prompt}]})

            config_dict = {}
            if self.system_prompt:
                config_dict["system_instruction"] = self.system_prompt
            if self.response_schema:
                config_dict["response_mime_type"] = "application/json"
                config_dict["response_schema"] = self.response_schema

            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config_dict if config_dict else None,
            )

            if self.response_schema:
                return json.loads(response.text)
            else:
                return response.text
        except Exception as e:
            raise RuntimeError(f"Antigravity Gemini real model error: {e}")

    def _run_mock(self, prompt: str, document: Optional[Document] = None, **kwargs) -> Any:
        if self.tools:
            import re
            query_match = re.search(r'Query:\s*(.+?)(?:\n|$)', prompt) or re.search(r'(.+)', prompt)
            if query_match:
                query = query_match.group(1).strip()
                for tool in self.tools:
                    try:
                        result = tool(query)
                        return json.loads(result) if isinstance(result, str) else result
                    except Exception:
                        continue
        if self.response_schema:
            return _construct_mock_response(self.response_schema, prompt)
        return {"result": "mock_output", "note": "NVIDIA_API_KEY / GEMINI_API_KEY not configured. Provide a valid key in backend/.env for real AI inference."}


__all__ = ["Agent", "Document"]
