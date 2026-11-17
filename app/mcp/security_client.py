
import asyncio
import os
import sys
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_role(role, tests):

    print(f"\n--- Testing role: {role} ---", flush=True)

    env = os.environ.copy()
    env["SENTINEL_ROLE"] = role

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.security_server"],
        env=env
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await asyncio.wait_for(
                session.initialize(),
                timeout=20
            )

            for tool_name, expected in tests:

                response = await asyncio.wait_for(
                    session.call_tool(tool_name, arguments={}),
                    timeout=20
                )

                data = response.structuredContent

                if data is None:
                    data = json.loads(response.content[0].text)

                actual = data.get("status")

                print(
                    f"{tool_name}: {actual} "
                    f"| Expected: {expected} "
                    f"| {'PASS' if actual == expected else 'FAIL'}",
                    flush=True
                )


async def main():

    await test_role(
        "employee",
        [
            ("read_security_policy", "ALLOWED"),
            ("read_network_record", "DENIED"),
            ("delete_network_record", "DENIED")
        ]
    )

    await test_role(
        "network_admin",
        [
            ("read_security_policy", "ALLOWED"),
            ("read_network_record", "ALLOWED"),
            ("delete_network_record", "DENIED")
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
