
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.security_server"]
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tests = [
                (
                    "Employee reads policy",
                    "read_security_policy",
                    {"role": "employee"},
                    "ALLOWED"
                ),
                (
                    "Employee reads restricted record",
                    "read_network_record",
                    {"role": "employee"},
                    "DENIED"
                ),
                (
                    "Admin reads restricted record",
                    "read_network_record",
                    {"role": "network_admin"},
                    "ALLOWED"
                ),
                (
                    "Employee attempts deletion",
                    "delete_network_record",
                    {"role": "employee"},
                    "DENIED"
                ),
                (
                    "Employee spoofs admin role",
                    "read_network_record",
                    {"role": "network_admin"},
                    "DENIED"
                )
            ]

            for name, tool, arguments, expected in tests:

                response = await session.call_tool(
                    tool,
                    arguments=arguments
                )

                data = response.structuredContent

                if data is None:
                    data = json.loads(
                        response.content[0].text
                    )

                actual = data.get("status")

                print("\nTest:", name)
                print("Expected:", expected)
                print("Actual:", actual)

                if actual == expected:
                    print("Result: PASS")
                else:
                    print("Result: FAIL")


if __name__ == "__main__":
    asyncio.run(main())
