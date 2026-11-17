
import json
from pathlib import Path
from datetime import datetime, timezone

from app.engines.redteam_engine import run_redteam_tests
from app.engines.rag_security_engine import assess_poisoning
from app.engines.leakage_engine import run_leakage_tests


def generate_report():

    print("\nStarting SENTINEL AI Security Assessment")

    # Execute existing Stage 2 engines
    redteam = run_redteam_tests()
    poisoning = assess_poisoning()
    leakage = run_leakage_tests()

    # Calculate observed exact canary/token disclosures
    redteam_leaks = sum(
        item["canary_leaked"] for item in redteam
    )

    poisoning_leaks = int(
        poisoning["canary_leaked"]
    )

    data_leaks = sum(
        item["secret_leaked"] for item in leakage
    )

    total_tests = len(redteam) + 1 + len(leakage)

    report = {
        "project": "SENTINEL AI",
        "stage": 2,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_tests": total_tests,
            "exact_secret_disclosures": (
                redteam_leaks
                + poisoning_leaks
                + data_leaks
            ),
            "note": (
                "Results cover exact synthetic secret "
                "disclosure only. They do not prove "
                "overall application security."
            )
        },
        "results": {
            "prompt_injection_and_jailbreak": redteam,
            "rag_poisoning": poisoning,
            "data_leakage": leakage
        }
    }

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    filename = (
        "stage2_report_"
        + datetime.now(timezone.utc).strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".json"
    )

    output_path = output_dir / filename

    output_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nAssessment completed")
    print("Total tests:", total_tests)
    print(
        "Exact secret disclosures:",
        report["summary"]["exact_secret_disclosures"]
    )
    print("Report saved:", output_path)

    return report


if __name__ == "__main__":
    generate_report()
