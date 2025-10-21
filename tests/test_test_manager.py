"""Tests for Test Manager"""

import pytest
import json
import tempfile
from pathlib import Path
from mcp_server.test_manager import TestManager, TestScenario


class TestTestManager:
    """Test the TestManager class"""

    def test_load_json_scenario(self):
        """Test loading a scenario from JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test scenario file
            scenario_data = {
                "id": "test_001",
                "title": "Test Scenario",
                "description": "A test scenario",
                "category": "basic",
                "difficulty": "easy",
                "context": "Test context",
                "requirements": ["req1", "req2"],
                "success_criteria": ["criteria1"],
                "test_cases": [
                    {
                        "input": "test",
                        "expected_output": "test",
                        "description": "test case"
                    }
                ],
                "language": "python"
            }

            scenario_file = Path(tmpdir) / "test_scenario.json"
            with open(scenario_file, 'w') as f:
                json.dump(scenario_data, f)

            # Load scenarios
            manager = TestManager(scenarios_dir=tmpdir)

            # Verify scenario was loaded
            assert len(manager.scenarios) == 1
            assert "test_001" in manager.scenarios

            scenario = manager.get_scenario("test_001")
            assert scenario is not None
            assert scenario.title == "Test Scenario"
            assert scenario.category == "basic"
            assert len(scenario.requirements) == 2

    def test_list_scenarios_by_category(self):
        """Test filtering scenarios by category"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple scenarios
            scenarios = [
                {"id": "basic_1", "title": "Basic 1", "category": "basic", "description": "test", "requirements": [], "success_criteria": [], "test_cases": []},
                {"id": "basic_2", "title": "Basic 2", "category": "basic", "description": "test", "requirements": [], "success_criteria": [], "test_cases": []},
                {"id": "adv_1", "title": "Advanced 1", "category": "advanced", "description": "test", "requirements": [], "success_criteria": [], "test_cases": []},
            ]

            for i, scenario_data in enumerate(scenarios):
                scenario_file = Path(tmpdir) / f"scenario_{i}.json"
                with open(scenario_file, 'w') as f:
                    json.dump(scenario_data, f)

            manager = TestManager(scenarios_dir=tmpdir)

            # Test filtering
            basic_scenarios = manager.list_scenarios(category="basic")
            assert len(basic_scenarios) == 2

            advanced_scenarios = manager.list_scenarios(category="advanced")
            assert len(advanced_scenarios) == 1

            all_scenarios = manager.list_scenarios()
            assert len(all_scenarios) == 3

    def test_get_nonexistent_scenario(self):
        """Test getting a scenario that doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TestManager(scenarios_dir=tmpdir)
            result = manager.get_scenario("nonexistent")
            assert result is None

    def test_add_scenario_programmatically(self):
        """Test adding a scenario programmatically"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = TestManager(scenarios_dir=tmpdir)

            new_scenario = TestScenario(
                id="prog_001",
                title="Programmatic Scenario",
                description="Added via code",
                category="test",
                difficulty="medium",
                context="test",
                requirements=["req1"],
                success_criteria=["criteria1"],
                test_cases=[],
                language="python"
            )

            manager.add_scenario(new_scenario)

            assert "prog_001" in manager.scenarios
            retrieved = manager.get_scenario("prog_001")
            assert retrieved.title == "Programmatic Scenario"

    def test_search_scenarios(self):
        """Test searching scenarios"""
        with tempfile.TemporaryDirectory() as tmpdir:
            scenarios = [
                {"id": "s1", "title": "Palindrome Checker", "description": "Check palindromes", "category": "basic", "requirements": [], "success_criteria": [], "test_cases": []},
                {"id": "s2", "title": "JSON Parser", "description": "Parse JSON data", "category": "basic", "requirements": [], "success_criteria": [], "test_cases": []},
                {"id": "s3", "title": "Binary Search", "description": "Implement binary search", "category": "basic", "requirements": [], "success_criteria": [], "test_cases": []},
            ]

            for i, scenario_data in enumerate(scenarios):
                scenario_file = Path(tmpdir) / f"scenario_{i}.json"
                with open(scenario_file, 'w') as f:
                    json.dump(scenario_data, f)

            manager = TestManager(scenarios_dir=tmpdir)

            # Search for "palindrome"
            results = manager.search_scenarios("palindrome")
            assert len(results) == 1
            assert results[0].id == "s1"

            # Search for "json"
            results = manager.search_scenarios("json")
            assert len(results) == 1
            assert results[0].id == "s2"

            # Search for "search"
            results = manager.search_scenarios("search")
            assert len(results) == 1
            assert results[0].id == "s3"
