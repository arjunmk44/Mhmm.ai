"""
LangGraph Failure Intelligence Agent for pattern detection and proactive safety scanning.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from ai_ml.agents.state import FailureScanState
from ai_ml.graph.neo4j_client import neo4j_client
from ai_ml.embeddings.vector_store import vector_store
from ai_ml.llm.model_router import model_router
from ai_ml.prompts.failure_analysis_prompt import FAILURE_ANALYSIS_SYSTEM_PROMPT, FAILURE_ANALYSIS_USER_PROMPT
from ai_ml.utils.helpers import parse_json_safely
from ai_ml.utils.logger import logger


def node_fetch_context(state: FailureScanState) -> Dict[str, Any]:
    eq_id = state.get("equipment_id") or "ALL_EQUIPMENT"
    
    # Fetch graph neighborhood
    g_context = neo4j_client.get_neighborhood(eq_id, depth=2)

    # Fetch vector chunks related to incidents / maintenance
    history = vector_store.similarity_search(f"incidents maintenance failures for {eq_id}", top_k=5)

    return {
        "graph_context": g_context,
        "historical_records": history,
        "error": None
    }


def node_analyze_patterns(state: FailureScanState) -> Dict[str, Any]:
    eq_id = state.get("equipment_id") or "ALL_EQUIPMENT"
    g_ctx = state.get("graph_context", {})
    history = state.get("historical_records", [])

    ctx_summary = f"Graph Nodes: {len(g_ctx.get('nodes', []))}, Graph Edges: {len(g_ctx.get('edges', []))}\n"
    ctx_summary += "Recent History Chunks:\n" + "\n".join([f"- {h.get('chunk_text', '')}" for h in history])

    prompt = FAILURE_ANALYSIS_USER_PROMPT.format(
        equipment_tag=eq_id,
        graph_and_historical_context=ctx_summary
    )

    result_json = model_router.generate_extraction(
        prompt=prompt,
        system_instruction=FAILURE_ANALYSIS_SYSTEM_PROMPT
    )

    risk_lvl = result_json.get("risk_level", "low")
    pot_failures = result_json.get("potential_failures", [])
    recs = result_json.get("recommendations", [])
    alerts = result_json.get("alerts", [])

    # Guarantee at least one structured alert payload if high or medium risk detected
    if not alerts and risk_lvl in ["high", "medium"]:
        alerts.append({
            "title": f"{risk_lvl.upper()} Risk Alert for {eq_id}",
            "description": f"Potential failure pattern identified in operational history for {eq_id}.",
            "severity": risk_lvl,
            "equipment_tag": eq_id
        })

    return {
        "analysis_payload": result_json,
        "risk_level": risk_lvl,
        "potential_failures": pot_failures,
        "recommendations": recs,
        "alerts": alerts
    }


def build_failure_scan_graph():
    workflow = StateGraph(FailureScanState)

    workflow.add_node("fetch_context", node_fetch_context)
    workflow.add_node("analyze_patterns", node_analyze_patterns)

    workflow.set_entry_point("fetch_context")
    workflow.add_edge("fetch_context", "analyze_patterns")
    workflow.add_edge("analyze_patterns", END)

    return workflow.compile()


failure_scan_agent_executor = build_failure_scan_graph()
