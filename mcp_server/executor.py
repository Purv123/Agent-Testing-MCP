"""
Safe Code Executor

Executes submitted code in isolated environments (Docker or subprocess)
with proper sandboxing and timeout controls.
"""

import asyncio
import logging
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

logger = logging.getLogger(__name__)


class CodeExecutor:
    """Executes code safely in isolated environments"""

    def __init__(self, use_docker: bool = None):
        """
        Initialize code executor

        Args:
            use_docker: Force Docker usage. If None, auto-detect availability.
        """
        if use_docker is None:
            self.use_docker = self._check_docker_available()
        else:
            self.use_docker = use_docker

        logger.info(f"Code executor initialized (Docker: {self.use_docker})")

    def _check_docker_available(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("Docker not available, falling back to subprocess execution")
            return False

    async def execute(
        self,
        code: str,
        language: str,
        test_cases: List[Dict[str, Any]],
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute code and run test cases

        Args:
            code: Source code to execute
            language: Programming language
            test_cases: List of test cases to validate
            timeout: Execution timeout in seconds

        Returns:
            Execution results including output, errors, and test results
        """
        if language == "python":
            return await self._execute_python(code, test_cases, timeout)
        elif language in ["javascript", "typescript"]:
            return await self._execute_javascript(code, test_cases, timeout, language)
        else:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "test_results": []
            }

    async def _execute_python(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout: int
    ) -> Dict[str, Any]:
        """Execute Python code"""
        if self.use_docker:
            return await self._execute_python_docker(code, test_cases, timeout)
        else:
            return await self._execute_python_subprocess(code, test_cases, timeout)

    async def _execute_python_subprocess(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout: int
    ) -> Dict[str, Any]:
        """Execute Python code using subprocess"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Write code to file
            code_file = tmppath / "solution.py"
            code_file.write_text(code)

            # Write test runner
            test_runner = tmppath / "test_runner.py"
            test_runner_code = self._generate_python_test_runner(test_cases)
            test_runner.write_text(test_runner_code)

            try:
                # Run the code
                process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    str(test_runner),
                    cwd=str(tmppath),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env={"PYTHONPATH": str(tmppath)}
                )

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )

                # Parse results
                output = stdout.decode()
                errors = stderr.decode()

                # Try to parse test results from output
                test_results = self._parse_test_results(output)

                return {
                    "success": process.returncode == 0,
                    "output": output,
                    "errors": errors,
                    "return_code": process.returncode,
                    "test_results": test_results
                }

            except asyncio.TimeoutError:
                logger.warning(f"Execution timeout after {timeout}s")
                return {
                    "success": False,
                    "error": f"Execution timeout ({timeout}s)",
                    "test_results": []
                }
            except Exception as e:
                logger.error(f"Execution error: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "test_results": []
                }

    async def _execute_python_docker(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout: int
    ) -> Dict[str, Any]:
        """Execute Python code in Docker container"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Write code and test runner
            code_file = tmppath / "solution.py"
            code_file.write_text(code)

            test_runner = tmppath / "test_runner.py"
            test_runner_code = self._generate_python_test_runner(test_cases)
            test_runner.write_text(test_runner_code)

            try:
                # Run in Docker
                process = await asyncio.create_subprocess_exec(
                    "docker", "run",
                    "--rm",
                    "--network", "none",
                    "--memory", "256m",
                    "--cpus", "1",
                    "-v", f"{tmppath}:/workspace:ro",
                    "-w", "/workspace",
                    "python:3.11-slim",
                    "python", "test_runner.py",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )

                output = stdout.decode()
                errors = stderr.decode()
                test_results = self._parse_test_results(output)

                return {
                    "success": process.returncode == 0,
                    "output": output,
                    "errors": errors,
                    "return_code": process.returncode,
                    "test_results": test_results,
                    "execution_environment": "docker"
                }

            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": f"Execution timeout ({timeout}s)",
                    "test_results": []
                }
            except Exception as e:
                logger.error(f"Docker execution error: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "test_results": []
                }

    async def _execute_javascript(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout: int,
        language: str
    ) -> Dict[str, Any]:
        """Execute JavaScript/TypeScript code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Write code
            ext = "ts" if language == "typescript" else "js"
            code_file = tmppath / f"solution.{ext}"
            code_file.write_text(code)

            # Write test runner
            test_runner = tmppath / "test_runner.js"
            test_runner_code = self._generate_js_test_runner(test_cases)
            test_runner.write_text(test_runner_code)

            try:
                cmd = ["node", "test_runner.js"]
                if language == "typescript":
                    cmd = ["ts-node", "test_runner.ts"]

                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=str(tmppath),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )

                output = stdout.decode()
                errors = stderr.decode()
                test_results = self._parse_test_results(output)

                return {
                    "success": process.returncode == 0,
                    "output": output,
                    "errors": errors,
                    "return_code": process.returncode,
                    "test_results": test_results
                }

            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": f"Execution timeout ({timeout}s)",
                    "test_results": []
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "test_results": []
                }

    def _generate_python_test_runner(self, test_cases: List[Dict[str, Any]]) -> str:
        """Generate Python test runner code"""
        # Convert test_cases to a Python repr string instead of JSON to preserve Python types
        test_cases_repr = repr(test_cases)
        return f'''
import json
import sys
import traceback
from solution import *

def run_tests():
    test_cases = {test_cases_repr}
    results = []

    for i, test_case in enumerate(test_cases):
        try:
            input_data = test_case.get("input")
            expected = test_case.get("expected_output")

            # Try to find and call the main function
            # Check globals() instead of dir() to find the main function
            if "main" not in globals():
                raise Exception("main() function not found in solution")

            if isinstance(input_data, dict):
                result = main(**input_data)
            elif isinstance(input_data, list):
                result = main(*input_data)
            else:
                result = main(input_data)

            passed = result == expected

            results.append({{
                "test_case": i + 1,
                "passed": passed,
                "input": input_data,
                "expected": expected,
                "actual": result,
                "description": test_case.get("description", "")
            }})
        except Exception as e:
            results.append({{
                "test_case": i + 1,
                "passed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }})

    print("===TEST_RESULTS===")
    print(json.dumps(results, indent=2))
    print("===END_TEST_RESULTS===")

    # Return exit code based on results
    all_passed = all(r.get("passed", False) for r in results)
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    run_tests()
'''

    def _generate_js_test_runner(self, test_cases: List[Dict[str, Any]]) -> str:
        """Generate JavaScript test runner code"""
        return f'''
const testCases = {json.dumps(test_cases)};

async function runTests() {{
    const results = [];

    for (let i = 0; i < testCases.length; i++) {{
        const testCase = testCases[i];
        try {{
            const input = testCase.input;
            const expected = testCase.expected_output;

            // Try to call main function
            const result = await main(input);
            const passed = JSON.stringify(result) === JSON.stringify(expected);

            results.push({{
                test_case: i + 1,
                passed,
                input,
                expected,
                actual: result,
                description: testCase.description || ""
            }});
        }} catch (e) {{
            results.push({{
                test_case: i + 1,
                passed: false,
                error: e.message,
                stack: e.stack
            }});
        }}
    }}

    console.log("===TEST_RESULTS===");
    console.log(JSON.stringify(results, null, 2));
    console.log("===END_TEST_RESULTS===");

    const allPassed = results.every(r => r.passed);
    process.exit(allPassed ? 0 : 1);
}}

runTests();
'''

    def _parse_test_results(self, output: str) -> List[Dict[str, Any]]:
        """Parse test results from output"""
        try:
            # Look for test results between markers
            if "===TEST_RESULTS===" in output and "===END_TEST_RESULTS===" in output:
                start = output.index("===TEST_RESULTS===") + len("===TEST_RESULTS===")
                end = output.index("===END_TEST_RESULTS===")
                results_json = output[start:end].strip()
                return json.loads(results_json)
        except Exception as e:
            logger.warning(f"Could not parse test results: {e}")

        return []
