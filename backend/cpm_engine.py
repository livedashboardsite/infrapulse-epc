
import networkx as nx
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from ground_truth import get_ground_truth_tasks


def create_cpm_graph(tasks: List[Dict[str, Any]]) -> Tuple[nx.DiGraph, Dict[int, Dict[str, Any]]]:
    G = nx.DiGraph()

    for task in tasks:
        G.add_node(
            task["id"],
            name=task["name"],
            duration=task["duration_days"],
            start_date=task["start_date"],
            end_date=task["end_date"],
            is_critical=task["is_critical"],
            resource_type=task["resource_type"],
            location=task["location"]
        )
        for dep in task["dependencies"]:
            G.add_edge(dep, task["id"])

    return G, {task["id"]: task for task in tasks}


def calculate_cpm(G: nx.DiGraph, tasks: Dict[int, Dict[str, Any]], delays: Dict[int, int] = None) -> Dict[str, Any]:
    if delays is None:
        delays = {}

    topo_order = list(nx.topological_sort(G))

    earliest_start = {}
    earliest_finish = {}

    for node in topo_order:
        duration = tasks[node]["duration_days"] + delays.get(node, 0)
        preds = list(G.predecessors(node))
        if not preds:
            earliest_start[node] = tasks[node]["start_date"]
        else:
            earliest_start[node] = max(earliest_finish[pred] for pred in preds)
        earliest_finish[node] = earliest_start[node] + timedelta(days=duration)

    latest_start = {}
    latest_finish = {}
    max_ef = max(earliest_finish.values())
    for node in reversed(topo_order):
        duration = tasks[node]["duration_days"] + delays.get(node, 0)
        succs = list(G.successors(node))
        if not succs:
            latest_finish[node] = max_ef
        else:
            latest_finish[node] = min(latest_start[succ] for succ in succs)
        latest_start[node] = latest_finish[node] - timedelta(days=duration)

    critical_path = []
    for node in topo_order:
        if earliest_start[node] == latest_start[node] and earliest_finish[node] == latest_finish[node]:
            critical_path.append(node)

    updated_tasks = []
    for node in topo_order:
        updated_tasks.append({
            **tasks[node],
            "duration_days": tasks[node]["duration_days"] + delays.get(node, 0),
            "start_date": earliest_start[node],
            "end_date": earliest_finish[node],
            "is_critical": node in critical_path
        })

    return {
        "tasks": updated_tasks,
        "critical_path": critical_path,
        "project_end_date": max_ef,
        "total_duration_days": (max_ef - tasks[1]["start_date"]).days
    }


def recalculate_with_delays(delays: Dict[int, int]) -> Dict[str, Any]:
    tasks = get_ground_truth_tasks()
    G, task_dict = create_cpm_graph(tasks)
    return calculate_cpm(G, task_dict, delays)

