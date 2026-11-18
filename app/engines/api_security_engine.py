
import httpx

BASE_URL = "http://127.0.0.1:8001"

SECRET = "SENTINEL-LAB-TOKEN-9C42"


def run_api_security_tests():

    tests = [
        {
            "name": "Public policy access",
            "path": "/public-policy",
            "headers": {},
            "expected": "PUBLIC"
        },
        {
            "name": "Employee restricted access",
            "path": "/network-record",
            "headers": {"X-Role": "employee"},
            "expected": "DENIED"
        },
        {
            "name": "Unverified admin role claim",
            "path": "/network-record",
            "headers": {"X-Role": "network_admin"},
            "expected": "DENIED"
        },
        {
            "name": "Invalid role access",
            "path": "/network-record",
            "headers": {"X-Role": "hacker"},
            "expected": "DENIED"
        }
    ]

    results = []

    with httpx.Client(timeout=10) as client:

        for test in tests:

            response = client.get(
                BASE_URL + test["path"],
                headers=test["headers"]
            )

            data = response.json()

            if test["expected"] == "PUBLIC":
                passed = response.status_code == 200
            else:
                passed = (
                    data.get("status") == "DENIED"
                    and SECRET not in response.text
                )

            result = {
                "test": test["name"],
                "http_status": response.status_code,
                "expected": test["expected"],
                "passed": passed,
                "secret_exposed": SECRET in response.text
            }

            results.append(result)

            print("\nTest:", result["test"])
            print("HTTP Status:", result["http_status"])
            print("Result:", "PASS" if passed else "FAIL")

    return results


if __name__ == "__main__":
    run_api_security_tests()
