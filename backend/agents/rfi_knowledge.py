
from typing import List, Dict, Any


MOCK_RFIS = [
    {
        "id": "RFI-001",
        "subject": "Cable tray routing in Data Hall A",
        "question": "Can we route 400V cables above fiber tray as per TIA-942?",
        "answer": "No, TIA-942 Section 8.2 specifies power and data segregation; maintain 300mm vertical separation.",
        "status": "Resolved",
        "citations": ["TIA-942 Section 8.2"],
        "date": "2024-01-15"
    },
    {
        "id": "RFI-002",
        "subject": "Battery room ventilation requirements",
        "question": "What is the required air change rate for VRLA battery room?",
        "answer": "Uptime Institute Tier III requires minimum 12 air changes per hour for battery rooms.",
        "status": "Resolved",
        "citations": ["Uptime Institute Tier III Standard"],
        "date": "2024-01-22"
    },
    {
        "id": "RFI-003",
        "subject": "CRAC unit redundancy",
        "question": "Is N+1 sufficient for CRAC units or do we need N+2?",
        "answer": "N+1 is acceptable for Tier III; however, N+2 is recommended for 2N distribution.",
        "status": "Resolved",
        "citations": ["TIA-942", "Uptime Tier III"],
        "date": "2024-02-01"
    }
]


def search_rfi(query: str) -> Dict[str, Any]:
    query_lower = query.lower()
    results = []

    for rfi in MOCK_RFIS:
        if (query_lower in rfi["subject"].lower() or
            query_lower in rfi["question"].lower() or
            query_lower in rfi["answer"].lower()):
            results.append(rfi)

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }


def get_past_rfis() -> List[Dict[str, Any]]:
    return MOCK_RFIS

