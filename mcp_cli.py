#!/usr/bin/env python3
"""
Command-line interface for the Agent Testing MCP Server

Usage:
    ./mcp_cli.py list-scenarios
    ./mcp_cli.py get-scenario basic_001
    ./mcp_cli.py submit basic_001 solution.py "My solution"
    ./mcp_cli.py execute solution.py
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server.test_manager import TestManager
from mcp_server.executor import CodeExecutor
from mcp_server.evaluator import TestEvaluator
from mcp_server.reporter import ResultReporter
import json
from datetime import datetime
from pathlib import Path


def list_scenarios():
    """List all available test scenarios"""
    manager = TestManager("./test_scenarios")

    print("\n📋 Available Test Scenarios:\n")
    print(f"{'ID':<20} {'Title':<50} {'Difficulty':<12} {'Category'}")
    print("=" * 100)

    for scenario_id, scenario in manager.scenarios.items():
        print(f"{scenario_id:<20} {scenario.title:<50} {scenario.difficulty:<12} {scenario.category}")

    print(f"\nTotal: {len(manager.scenarios)} scenarios\n")


def get_scenario(scenario_id):
    """Get detailed information about a specific scenario"""
    manager = TestManager("./test_scenarios")

    scenario = manager.get_scenario(scenario_id)
    if not scenario:
        print(f"❌ Scenario '{scenario_id}' not found")
        return

    print(f"\n{'='*80}")
    print(f"📝 {scenario.title}")
    print(f"{'='*80}\n")
    print(f"ID: {scenario.id}")
    print(f"Category: {scenario.category}")
    print(f"Difficulty: {scenario.difficulty}")
    print(f"Language: {scenario.language}")
    print(f"\n📖 Description:\n{scenario.description}\n")
    print(f"🎯 Context:\n{scenario.context}\n")

    print("✅ Requirements:")
    for i, req in enumerate(scenario.requirements, 1):
        print(f"  {i}. {req}")

    print(f"\n🧪 Test Cases: {len(scenario.test_cases)} cases")
    for i, tc in enumerate(scenario.test_cases, 1):
        print(f"  {i}. {tc.get('description', 'Test case')}")
        print(f"     Input: {tc.get('input')}")
        print(f"     Expected: {tc.get('expected_output')}")

    if scenario.starter_code:
        print(f"\n💡 Starter Code:\n")
        print("```" + scenario.language)
        print(scenario.starter_code)
        print("```\n")

    if scenario.hints:
        print("💡 Hints:")
        for i, hint in enumerate(scenario.hints, 1):
            print(f"  {i}. {hint}")

    print()


def submit_solution(scenario_id, code_file, explanation=""):
    """Submit a solution for evaluation"""
    # Load scenario
    manager = TestManager("./test_scenarios")
    scenario = manager.get_scenario(scenario_id)

    if not scenario:
        print(f"❌ Scenario '{scenario_id}' not found")
        return

    # Read code
    if not os.path.exists(code_file):
        print(f"❌ Code file '{code_file}' not found")
        return

    with open(code_file, 'r') as f:
        code = f.read()

    print(f"\n🚀 Submitting solution for: {scenario.title}\n")

    # Execute code
    executor = CodeExecutor()
    print("⏳ Executing code...")
    execution_result = executor.execute_code(code, scenario.language, scenario.timeout)

    if execution_result["status"] == "error":
        print(f"❌ Execution Error:\n{execution_result['error']}\n")
        return

    # Run tests
    print("🧪 Running test cases...")
    test_results = executor.run_test_cases(code, scenario.test_cases, scenario.language)

    # Evaluate
    evaluator = TestEvaluator()
    print("📊 Evaluating solution...")
    evaluation = evaluator.evaluate_submission(
        scenario=scenario,
        code=code,
        execution_result=execution_result,
        test_results=test_results,
        explanation=explanation
    )

    # Generate report
    run_id = f"{scenario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    reporter = ResultReporter()

    result = {
        "run_id": run_id,
        "scenario_id": scenario_id,
        "scenario_title": scenario.title,
        "timestamp": datetime.now().isoformat(),
        "code": code,
        "language": scenario.language,
        "explanation": explanation,
        "execution": execution_result,
        "test_results": test_results,
        "evaluation": evaluation
    }

    # Save results
    os.makedirs("results", exist_ok=True)
    reporter.save_json_result(result, f"results/{run_id}.json")
    reporter.generate_markdown_report(result, f"results/{run_id}.md")

    # Print summary
    print("\n" + "="*80)
    print(f"📊 Test Results Summary")
    print("="*80 + "\n")

    status = "✅ PASSED" if evaluation["overall_pass"] else "❌ FAILED"
    print(f"Status: {status}")
    print(f"Score: {evaluation['overall_score']:.2f}/1.00")
    print(f"Threshold: {evaluation.get('pass_threshold', 0.7):.2f}")

    print(f"\n📈 Metrics:")
    for metric, score in evaluation["scores"].items():
        bar_length = int(score * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"  {metric.capitalize():<15} {bar} {score:.2f}")

    print(f"\n🧪 Test Cases: {test_results['passed']}/{test_results['total']} passed")

    if test_results.get("failures"):
        print("\n❌ Failed Tests:")
        for failure in test_results["failures"]:
            print(f"  • {failure.get('description', 'Test')}")
            print(f"    Expected: {failure.get('expected')}")
            print(f"    Got: {failure.get('actual')}")

    print(f"\n💾 Results saved:")
    print(f"  • JSON: results/{run_id}.json")
    print(f"  • Report: results/{run_id}.md")
    print()


def execute_code(code_file, language="python"):
    """Execute code without evaluation"""
    if not os.path.exists(code_file):
        print(f"❌ Code file '{code_file}' not found")
        return

    with open(code_file, 'r') as f:
        code = f.read()

    print(f"\n⚡ Executing {language} code...\n")

    executor = CodeExecutor()
    result = executor.execute_code(code, language, timeout=30)

    if result["status"] == "success":
        print("✅ Execution successful\n")
        if result.get("stdout"):
            print("📤 Output:")
            print(result["stdout"])
        if result.get("stderr"):
            print("\n⚠️  Stderr:")
            print(result["stderr"])
    else:
        print("❌ Execution failed\n")
        print(result.get("error", "Unknown error"))

    print(f"\nExecution time: {result.get('execution_time', 0):.3f}s\n")


def show_usage():
    """Show usage information"""
    print("""
🧪 Agent Testing MCP - Command Line Interface

Usage:
    ./mcp_cli.py list                           List all scenarios
    ./mcp_cli.py get <scenario_id>              Get scenario details
    ./mcp_cli.py submit <scenario_id> <file>    Submit solution
    ./mcp_cli.py execute <file>                 Execute code
    ./mcp_cli.py help                           Show this help

Examples:
    # List all available test scenarios
    ./mcp_cli.py list

    # View scenario details
    ./mcp_cli.py get basic_001

    # Submit a solution
    ./mcp_cli.py submit basic_001 my_solution.py

    # Just execute code without testing
    ./mcp_cli.py execute my_code.py
""")


def main():
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command in ["list", "ls"]:
            list_scenarios()
        elif command in ["get", "show", "info"]:
            if len(sys.argv) < 3:
                print("❌ Usage: ./mcp_cli.py get <scenario_id>")
                sys.exit(1)
            get_scenario(sys.argv[2])
        elif command == "submit":
            if len(sys.argv) < 4:
                print("❌ Usage: ./mcp_cli.py submit <scenario_id> <code_file> [explanation]")
                sys.exit(1)
            explanation = sys.argv[4] if len(sys.argv) > 4 else ""
            submit_solution(sys.argv[2], sys.argv[3], explanation)
        elif command == "execute":
            if len(sys.argv) < 3:
                print("❌ Usage: ./mcp_cli.py execute <code_file>")
                sys.exit(1)
            execute_code(sys.argv[2])
        elif command in ["help", "-h", "--help"]:
            show_usage()
        else:
            print(f"❌ Unknown command: {command}")
            show_usage()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
