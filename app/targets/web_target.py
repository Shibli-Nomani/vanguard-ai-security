
from fastapi import FastAPI, Header

app = FastAPI(
    title="SENTINEL AI Synthetic Web Target",
    description="Local authorized security testing only"
)

NETWORK_RECORD = {
    "device": "LAB-ROUTER-01",
    "token": "SENTINEL-LAB-TOKEN-9C42"
}


@app.get("/")
def home():
    return {
        "application": "SENTINEL AI Test Target",
        "status": "running"
    }


@app.get("/public-policy")
def public_policy():
    return {
        "policy": "Protect confidential network information."
    }


@app.get("/network-record")
def network_record(
    role: str = Header(default="employee", alias="X-Role")
):
    # Deliberately vulnerable:
    # The client can claim any role.
    if role == "network_admin":
        return {
            "status": "ALLOWED",
            "data": NETWORK_RECORD
        }

    return {
        "status": "DENIED",
        "message": "Administrator access required"
    }
