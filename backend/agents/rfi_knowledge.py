import json
import os
from typing import List, Dict, Any
from google.antigravity import Agent


RFI_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "rfis.json")


def _load_rfis() -> List[Dict[str, Any]]:
    with open(RFI_DATA_PATH, "r") as f:
        return json.load(f)


def _search_rfi_tool(query: str) -> str:
    rfis = _load_rfis()
    query_lower = query.lower()
    results = []

    for rfi in rfis:
        relevance = 0
        search_space = (
            rfi.get("subject", "").lower() + " " +
            rfi.get("question", "").lower() + " " +
            rfi.get("answer", "").lower() + " " +
            " ".join(rfi.get("citations", [])).lower()
        )
        query_terms = query_lower.split()
        for term in query_terms:
            if term in search_space:
                relevance += 1

        if relevance > 0:
            results.append({"rfi": rfi, "relevance": relevance})

    results.sort(key=lambda x: x["relevance"], reverse=True)
    top_results = results[:5]

    if not top_results:
        return json.dumps({"query": query, "results": [], "note": "No matching RFIs found in the database."})

    output = {"query": query, "total_results": len(top_results), "results": [r["rfi"] for r in top_results]}
    return json.dumps(output, indent=2)


RFI_AGENT = Agent(
    model="gemini-2.0-flash",
    tools=[_search_rfi_tool],
    system_prompt=(
        "You are an RFI and Project Knowledge Agent for data centre EPC projects. "
        "You have access to a search tool that queries a database of past RFIs and TIA-942/Uptime Institute standards. "
        "When asked a question, use the search tool to find relevant RFIs and standards, "
        "then synthesize a comprehensive answer referencing citations. "
        "If the search returns no results, state that the information is not in the knowledge base."
    ),
)


def search_rfi(query: str) -> Dict[str, Any]:
    prompt = (
        f"Query: {query}\n\n"
        f"Search the RFI knowledge base for relevant entries. Synthesize the answer using "
        f"the search results, referencing specific RFI IDs and standard citations where applicable."
    )
    result = RFI_AGENT.run(prompt=prompt)

    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"query": query, "total_results": 1, "results": [{"answer": result}]}
    return result


def get_past_rfis() -> List[Dict[str, Any]]:
    return _load_rfis()
