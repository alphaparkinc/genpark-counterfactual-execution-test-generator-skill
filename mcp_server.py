"""
MCP Server for Counterfactual Execution Test Generator Skill.
"""

import json
import sys
from client import CounterfactualTestGenerator

GENERATOR = CounterfactualTestGenerator()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "synthesize_test_suite",
                    "description": "Generate counterfactual edge-case inputs for tool schema parameters",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "param_schema": {"type": "object"},
                            "max_tests": {"type": "integer", "default": 10}
                        },
                        "required": ["param_schema"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "synthesize_test_suite":
            res = GENERATOR.synthesize_test_suite(
                args["param_schema"],
                args.get("max_tests", 10)
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
