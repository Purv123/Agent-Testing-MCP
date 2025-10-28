"""
Main MCP Server Implementation

Exposes tools for AI agents to interact with test scenarios,
submit solutions, and receive evaluations.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .test_manager import TestManager
from .executor import CodeExecutor
from .evaluator import TestEvaluator
from .reporter import ResultReporter

# Configure logging - ONLY to file (not stderr) to avoid interfering with MCP stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mcp_server.log')
    ]
)
logger = logging.getLogger(__name__)


class AgentTestingServer:
    """MCP Server for AI Agent Testing"""

    def __init__(self):
        self.server = Server("agent-testing-server")
        self.test_manager = TestManager()
        self.executor = CodeExecutor()
        self.evaluator = TestEvaluator()
        self.reporter = ResultReporter()

        # Setup tool handlers
        self._register_handlers()

        logger.info("Agent Testing Server initialized")

    def _register_handlers(self):
        """Register MCP tool handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available MCP tools"""
            return [
                Tool(
                    name="list_test_scenarios",
                    description="List all available test scenarios for AI agents to attempt",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Filter by category (optional)",
                                "enum": ["basic", "intermediate", "advanced", "bug_fix", "refactoring"]
                            }
                        }
                    }
                ),
                Tool(
                    name="get_test_scenario",
                    description="Get detailed information about a specific test scenario including setup, requirements, and success criteria",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scenario_id": {
                                "type": "string",
                                "description": "The unique ID of the test scenario"
                            }
                        },
                        "required": ["scenario_id"]
                    }
                ),
                Tool(
                    name="submit_solution",
                    description="Submit your solution for a test scenario to be executed and evaluated",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scenario_id": {
                                "type": "string",
                                "description": "The test scenario ID"
                            },
                            "code": {
                                "type": "string",
                                "description": "Your solution code"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language",
                                "enum": ["python", "javascript", "typescript", "java", "go"]
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Optional explanation of your approach"
                            }
                        },
                        "required": ["scenario_id", "code", "language"]
                    }
                ),
                Tool(
                    name="execute_code",
                    description="Execute code in a safe sandbox environment and get the output",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Code to execute"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language",
                                "enum": ["python", "javascript", "typescript"]
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Execution timeout in seconds (default: 30)",
                                "default": 30
                            }
                        },
                        "required": ["code", "language"]
                    }
                ),
                Tool(
                    name="get_test_results",
                    description="Get the evaluation results for a submitted test run",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "run_id": {
                                "type": "string",
                                "description": "The test run ID returned from submit_solution"
                            }
                        },
                        "required": ["run_id"]
                    }
                ),
                Tool(
                    name="list_test_runs",
                    description="List all test runs with their status and scores",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scenario_id": {
                                "type": "string",
                                "description": "Filter by scenario ID (optional)"
                            },
                            "status": {
                                "type": "string",
                                "description": "Filter by status (optional)",
                                "enum": ["passed", "failed", "error"]
                            }
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
            """Handle tool calls"""
            logger.info(f"Tool called: {name} with arguments: {arguments}")

            try:
                if name == "list_test_scenarios":
                    result = await self._list_test_scenarios(arguments)
                elif name == "get_test_scenario":
                    result = await self._get_test_scenario(arguments)
                elif name == "submit_solution":
                    result = await self._submit_solution(arguments)
                elif name == "execute_code":
                    result = await self._execute_code(arguments)
                elif name == "get_test_results":
                    result = await self._get_test_results(arguments)
                elif name == "list_test_runs":
                    result = await self._list_test_runs(arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]

    async def _list_test_scenarios(self, args: dict) -> dict:
        """List available test scenarios"""
        category = args.get("category")
        scenarios = self.test_manager.list_scenarios(category=category)

        return {
            "scenarios": [
                {
                    "id": s.id,
                    "title": s.title,
                    "category": s.category,
                    "difficulty": s.difficulty,
                    "description": s.description
                }
                for s in scenarios
            ],
            "total": len(scenarios)
        }

    async def _get_test_scenario(self, args: dict) -> dict:
        """Get detailed test scenario"""
        scenario_id = args["scenario_id"]
        scenario = self.test_manager.get_scenario(scenario_id)

        if not scenario:
            return {"error": f"Scenario not found: {scenario_id}"}

        return {
            "id": scenario.id,
            "title": scenario.title,
            "category": scenario.category,
            "difficulty": scenario.difficulty,
            "description": scenario.description,
            "context": scenario.context,
            "requirements": scenario.requirements,
            "success_criteria": scenario.success_criteria,
            "test_cases": scenario.test_cases,
            "starter_code": scenario.starter_code,
            "hints": scenario.hints
        }

    async def _submit_solution(self, args: dict) -> dict:
        """Submit and evaluate a solution"""
        scenario_id = args["scenario_id"]
        code = args["code"]
        language = args["language"]
        explanation = args.get("explanation", "")

        scenario = self.test_manager.get_scenario(scenario_id)
        if not scenario:
            return {"error": f"Scenario not found: {scenario_id}"}

        # Generate run ID
        run_id = f"{scenario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Execute code
        logger.info(f"Executing solution for {scenario_id}")
        execution_result = await self.executor.execute(
            code=code,
            language=language,
            test_cases=scenario.test_cases,
            timeout=scenario.timeout
        )

        # Evaluate solution
        logger.info(f"Evaluating solution for {scenario_id}")
        evaluation = await self.evaluator.evaluate(
            scenario=scenario,
            code=code,
            execution_result=execution_result,
            explanation=explanation
        )

        # Generate report
        report = self.reporter.create_report(
            run_id=run_id,
            scenario=scenario,
            code=code,
            execution_result=execution_result,
            evaluation=evaluation,
            explanation=explanation
        )

        # Save results
        self.reporter.save_results(run_id, report)

        return {
            "run_id": run_id,
            "status": evaluation["status"],
            "passed": evaluation["passed"],
            "score": evaluation["overall_score"],
            "summary": evaluation["summary"],
            "execution": {
                "success": execution_result["success"],
                "output": execution_result.get("output", ""),
                "errors": execution_result.get("errors", "")
            },
            "message": "Solution evaluated successfully. Use get_test_results for detailed report."
        }

    async def _execute_code(self, args: dict) -> dict:
        """Execute code in sandbox"""
        code = args["code"]
        language = args["language"]
        timeout = args.get("timeout", 30)

        result = await self.executor.execute(
            code=code,
            language=language,
            test_cases=[],
            timeout=timeout
        )

        return result

    async def _get_test_results(self, args: dict) -> dict:
        """Get detailed test results"""
        run_id = args["run_id"]
        results = self.reporter.load_results(run_id)

        if not results:
            return {"error": f"Results not found for run_id: {run_id}"}

        return results

    async def _list_test_runs(self, args: dict) -> dict:
        """List all test runs"""
        scenario_id = args.get("scenario_id")
        status = args.get("status")

        runs = self.reporter.list_runs(scenario_id=scenario_id, status=status)

        return {
            "runs": runs,
            "total": len(runs)
        }

    async def run(self):
        """Start the MCP server"""
        logger.info("Starting Agent Testing MCP Server...")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = AgentTestingServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
