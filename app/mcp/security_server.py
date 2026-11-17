
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SENTINEL Security MCP")

POLICY = "Confidential data is available only to authorized users."

NETWORK_RECORD = {
    "device": "LAB-ROUTER-01",
    "token": "SENTINEL-LAB-TOKEN-9C42"
}

# Local lab identity: configured when server starts
SERVER_ROLE = os.getenv("SENTINEL_ROLE", "employee")

ROLE_PERMISSIONS = {
    "employee": {
        "read_security_policy"
    },
    "network_admin": {
        "read_security_policy",
        "read_network_record"
    }
}


def authorized(operation):
    permissions = ROLE_PERMISSIONS.get(SERVER_ROLE, set())
    return operation in permissions


@mcp.tool()
def read_security_policy() -> dict:
    """Read the synthetic company security policy."""

    if not authorized("read_security_policy"):
        return {"status": "DENIED"}

    return {
        "status": "ALLOWED",
        "data": POLICY
    }


@mcp.tool()
def read_network_record() -> dict:
    """Read a restricted synthetic network record."""

    if not authorized("read_network_record"):
        return {"status": "DENIED"}

    return {
        "status": "ALLOWED",
        "data": NETWORK_RECORD
    }


@mcp.tool()
def delete_network_record() -> dict:
    """Attempt a prohibited synthetic delete operation."""

    return {
        "status": "DENIED",
        "reason": "Delete operations are disabled"
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
