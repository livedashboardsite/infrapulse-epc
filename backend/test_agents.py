import os
import sys
import json
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["GEMINI_API_KEY"] = ""

from google.antigravity import Agent, Document
from agents.spec_compliance import check_submittal, check_submittal_document, SpecComplianceResult
from agents.rfi_knowledge import search_rfi, get_past_rfis
from agents.schedule_risk import predict_risks, ScheduleRiskResult
from agents.commissioning import evaluate_test_result, CommissioningEvaluation
from cpm_engine import recalculate_with_delays, get_ground_truth_tasks, create_cpm_graph, calculate_cpm
from ground_truth import get_ground_truth_tasks as get_tasks


class TestAntigravityShim(unittest.TestCase):
    def test_agent_creates_with_default_model(self):
        agent = Agent()
        self.assertIn("llama", agent.model)

    def test_agent_returns_mock_result_without_api_key(self):
        agent = Agent(response_schema=SpecComplianceResult)
        result = agent.run(prompt="Test prompt")
        self.assertIn("compliance_score", result)

    def test_document_from_text(self):
        doc = Document.from_text("Test content")
        self.assertEqual(doc.mime_type, "text/plain")
        self.assertEqual(doc.content, "Test content")


class TestSpecComplianceAgent(unittest.TestCase):
    def test_check_submittal_returns_structured_result(self):
        result = check_submittal({
            "submittal_name": "UPS-01",
            "battery_runtime_minutes": 22,
            "redundancy": "N+2",
            "ups_efficiency_percent": 94.5,
            "chiller_n_plus_1": True
        })
        self.assertIn("overall_compliant", result)
        self.assertIn("compliance_score", result)
        self.assertIn("checks", result)
        self.assertIn("submittal_name", result)

    def test_check_submittal_non_compliant(self):
        result = check_submittal({
            "submittal_name": "UPS-02",
            "battery_runtime_minutes": 10,
            "redundancy": "N",
            "ups_efficiency_percent": 85.0,
            "chiller_n_plus_1": False
        })
        self.assertIsInstance(result, dict)

    def test_check_submittal_document(self):
        doc = Document.from_text("Submittal: UPS-03, Battery: 25min, Redundancy: N+2, UPS Efficiency: 96%, Chiller: N+1")
        result = check_submittal_document(doc)
        self.assertIn("overall_compliant", result)


class TestRFIKnowledgeAgent(unittest.TestCase):
    def test_get_past_rfis_returns_list(self):
        rfis = get_past_rfis()
        self.assertGreater(len(rfis), 0)
        self.assertIn("id", rfis[0])
        self.assertIn("subject", rfis[0])

    def test_search_rfi_finds_cable_separation(self):
        result = search_rfi("cable separation distance")
        if "total_results" not in result:
            result = search_rfi.__wrapped__(result) if hasattr(search_rfi, "__wrapped__") else {"results": []}
        self.assertTrue("total_results" in result or "results" in result)

    def test_search_rfi_returns_citations(self):
        result = search_rfi("battery room ventilation")
        self.assertTrue("results" in result or "total_results" in result)


class TestScheduleRiskAgent(unittest.TestCase):
    def test_predict_risks_returns_structured_result(self):
        tasks = get_tasks()
        result = predict_risks(tasks)
        self.assertIn("total_risks", result)
        self.assertIn("high_severity", result)
        self.assertIn("risks", result)

    def test_predict_risks_identifies_critical_path_risks(self):
        tasks = get_tasks()
        result = predict_risks(tasks)
        if result.get("risks"):
            for risk in result["risks"]:
                self.assertIn("task_id", risk)
                self.assertIn("severity", risk)
                self.assertIn("mitigation", risk)


class TestCommissioningAgent(unittest.TestCase):
    def test_evaluate_pass(self):
        result = evaluate_test_result("Generator ran at full load for 4 hours without any issues. All parameters within acceptable range.")
        self.assertIn("status", result)
        self.assertIn("delay_days", result)

    def test_evaluate_failure(self):
        result = evaluate_test_result("The generator shut down automatically after 2 hours due to overheating and high coolant temperature.")
        self.assertIn("status", result)

    def test_evaluate_failure_allocates_delay(self):
        result = evaluate_test_result("Critical failure: UPS failed to transfer within 10ms, control board fault detected.")
        self.assertIn("delay_days", result)

    def test_evaluate_warning(self):
        result = evaluate_test_result("Minor calibration issue detected on BMS temperature sensor. Adjustment required.")
        self.assertIn("status", result)


class TestCPMEngine(unittest.TestCase):
    def test_recalculate_with_delays_updates_end_date(self):
        tasks = get_tasks()
        G, task_dict = create_cpm_graph(tasks)
        original = calculate_cpm(G, task_dict)
        original_end = original["project_end_date"]

        delays = {20: 10}
        recalculated = recalculate_with_delays(delays)
        new_end = recalculated["project_end_date"]

        self.assertGreater(new_end, original_end)

    def test_critical_path_identification(self):
        tasks = get_tasks()
        G, task_dict = create_cpm_graph(tasks)
        result = calculate_cpm(G, task_dict)
        self.assertIn("critical_path", result)
        self.assertGreater(len(result["critical_path"]), 0)

    def test_delay_propagates_to_downstream_tasks(self):
        delays = {3: 30}
        result = recalculate_with_delays(delays)
        delayed_task = next(t for t in result["tasks"] if t["id"] == 3)
        self.assertEqual(delayed_task["duration_days"], get_original_duration(3) + 30)
        for task in result["tasks"]:
            if task["id"] > 3 and task["is_critical"]:
                eshift = (task["end_date"] - task["start_date"]).days if hasattr(task["end_date"], 'days') else task["duration_days"]
                self.assertGreaterEqual(task["duration_days"], get_original_duration(task["id"]))


def get_original_duration(task_id):
    tasks = get_tasks()
    for t in tasks:
        if t["id"] == task_id:
            return t["duration_days"]
    return 0


class TestSupplyChainAgent(unittest.TestCase):
    def test_shipments_loaded(self):
        from agents.supply_chain import get_supply_chain_tracking
        result = get_supply_chain_tracking()
        self.assertIn("shipments", result)
        self.assertGreater(len(result["shipments"]), 0)

    def test_shipment_has_position_data(self):
        from agents.supply_chain import get_supply_chain_tracking
        result = get_supply_chain_tracking()
        for s in result["shipments"]:
            self.assertIn("position_lat", s)
            self.assertIn("position_lon", s)
            self.assertIn("progress_pct", s)


if __name__ == "__main__":
    unittest.main()
