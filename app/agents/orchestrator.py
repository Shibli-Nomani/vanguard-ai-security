
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.engines.redteam_engine import run_redteam_tests
from app.engines.rag_security_engine import assess_poisoning
from app.engines.leakage_engine import run_leakage_tests


# Shared memory for our four agents
class SecurityState(TypedDict, total=False):
    redteam_results: list
    rag_results: dict
    leakage_results: list
    evidence: dict
    report_path: str


# Agent 1: Red Team
def redteam_agent(state: SecurityState):

    print("\n[Agent 1] Running Red Team Tests")

    results = run_redteam_tests()

    return {"redteam_results": results}


# Agent 2: RAG Security
def rag_security_agent(state: SecurityState):

    print("\n[Agent 2] Running RAG Security Tests")

    poisoning = assess_poisoning()
    leakage = run_leakage_tests()

    return {
        "rag_results": poisoning,
        "leakage_results": leakage
    }


# Agent 3: Evidence Collection
def evidence_agent(state: SecurityState):

    print("\n[Agent 3] Collecting Evidence")

    redteam = state["redteam_results"]
    rag = state["rag_results"]
    leakage = state["leakage_results"]

    total_tests = len(redteam) + 1 + len(leakage)

    confirmed_leaks = (
        sum(x["canary_leaked"] for x in redteam)
        + int(rag["canary_leaked"])
        + sum(x["secret_leaked"] for x in leakage)
    )

    evidence = {
        "total_tests": total_tests,
        "confirmed_exact_disclosures": confirmed_leaks,
        "redteam": redteam,
        "rag_poisoning": rag,
        "data_leakage": leakage
    }

    return {"evidence": evidence}


# Agent 4: Report Generation
def report_agent(state: SecurityState):

    print("\n[Agent 4] Generating Report")

    report = {
        "project": "SENTINEL AI",
        "stage": 3,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_tests": state["evidence"]["total_tests"],
            "confirmed_exact_disclosures": (
                state["evidence"]["confirmed_exact_disclosures"]
            )
        },
        "evidence": state["evidence"]
    }

    Path("reports").mkdir(exist_ok=True)

    filename = (
        "reports/langgraph_report_"
        + datetime.now(timezone.utc).strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        + ".json"
    )

    Path(filename).write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("Report saved:", filename)

    return {"report_path": filename}


# Create LangGraph workflow
workflow = StateGraph(SecurityState)

workflow.add_node("redteam", redteam_agent)
workflow.add_node("rag_security", rag_security_agent)
workflow.add_node("evidence", evidence_agent)
workflow.add_node("report", report_agent)

workflow.add_edge(START, "redteam")
workflow.add_edge("redteam", "rag_security")
workflow.add_edge("rag_security", "evidence")
workflow.add_edge("evidence", "report")
workflow.add_edge("report", END)

app = workflow.compile()


if __name__ == "__main__":

    print("\nSENTINEL AI - Multi-Agent Security Assessment")

    result = app.invoke({})

    print("\nAssessment completed")
    print("Final report:", result["report_path"])
