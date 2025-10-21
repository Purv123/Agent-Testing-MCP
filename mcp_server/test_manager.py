"""
Test Scenario Manager

Handles loading, parsing, and managing test scenarios from JSON/YAML files.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import yaml

logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """Individual test case for validation"""
    input: Any
    expected_output: Any
    description: str = ""


@dataclass
class TestScenario:
    """Complete test scenario definition"""
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    context: str
    requirements: List[str]
    success_criteria: List[str]
    test_cases: List[Dict[str, Any]]
    language: str = "python"
    starter_code: Optional[str] = None
    hints: List[str] = field(default_factory=list)
    timeout: int = 30
    evaluation_metrics: Dict[str, Any] = field(default_factory=dict)
    prerequisites: Dict[str, Any] = field(default_factory=dict)


class TestManager:
    """Manages test scenarios for AI agent testing"""

    def __init__(self, scenarios_dir: str = "test_scenarios"):
        self.scenarios_dir = Path(scenarios_dir)
        self.scenarios: Dict[str, TestScenario] = {}
        self._load_scenarios()

    def _load_scenarios(self):
        """Load all test scenarios from the scenarios directory"""
        if not self.scenarios_dir.exists():
            logger.warning(f"Scenarios directory not found: {self.scenarios_dir}")
            self.scenarios_dir.mkdir(parents=True, exist_ok=True)
            return

        # Load JSON files
        for file_path in self.scenarios_dir.glob("*.json"):
            try:
                self._load_scenario_file(file_path, format="json")
            except Exception as e:
                logger.error(f"Error loading scenario {file_path}: {e}")

        # Load YAML files
        for file_path in self.scenarios_dir.glob("*.yaml"):
            try:
                self._load_scenario_file(file_path, format="yaml")
            except Exception as e:
                logger.error(f"Error loading scenario {file_path}: {e}")

        for file_path in self.scenarios_dir.glob("*.yml"):
            try:
                self._load_scenario_file(file_path, format="yaml")
            except Exception as e:
                logger.error(f"Error loading scenario {file_path}: {e}")

        logger.info(f"Loaded {len(self.scenarios)} test scenarios")

    def _load_scenario_file(self, file_path: Path, format: str = "json"):
        """Load a single scenario file"""
        with open(file_path, 'r') as f:
            if format == "json":
                data = json.load(f)
            else:
                data = yaml.safe_load(f)

        # Handle both single scenario and multiple scenarios in one file
        if isinstance(data, list):
            for scenario_data in data:
                scenario = self._parse_scenario(scenario_data)
                self.scenarios[scenario.id] = scenario
                logger.info(f"Loaded scenario: {scenario.id} - {scenario.title}")
        else:
            scenario = self._parse_scenario(data)
            self.scenarios[scenario.id] = scenario
            logger.info(f"Loaded scenario: {scenario.id} - {scenario.title}")

    def _parse_scenario(self, data: Dict[str, Any]) -> TestScenario:
        """Parse scenario data into TestScenario object"""
        return TestScenario(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data.get("category", "general"),
            difficulty=data.get("difficulty", "medium"),
            context=data.get("context", ""),
            requirements=data.get("requirements", []),
            success_criteria=data.get("success_criteria", []),
            test_cases=data.get("test_cases", []),
            language=data.get("language", "python"),
            starter_code=data.get("starter_code"),
            hints=data.get("hints", []),
            timeout=data.get("timeout", 30),
            evaluation_metrics=data.get("evaluation_metrics", {}),
            prerequisites=data.get("prerequisites", {})
        )

    def list_scenarios(self, category: Optional[str] = None) -> List[TestScenario]:
        """List all scenarios, optionally filtered by category"""
        scenarios = list(self.scenarios.values())

        if category:
            scenarios = [s for s in scenarios if s.category == category]

        return sorted(scenarios, key=lambda s: s.id)

    def get_scenario(self, scenario_id: str) -> Optional[TestScenario]:
        """Get a specific scenario by ID"""
        return self.scenarios.get(scenario_id)

    def reload_scenarios(self):
        """Reload all scenarios from disk"""
        self.scenarios.clear()
        self._load_scenarios()

    def add_scenario(self, scenario: TestScenario):
        """Add a scenario programmatically"""
        self.scenarios[scenario.id] = scenario
        logger.info(f"Added scenario: {scenario.id}")

    def remove_scenario(self, scenario_id: str) -> bool:
        """Remove a scenario"""
        if scenario_id in self.scenarios:
            del self.scenarios[scenario_id]
            logger.info(f"Removed scenario: {scenario_id}")
            return True
        return False

    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return sorted(set(s.category for s in self.scenarios.values()))

    def search_scenarios(self, query: str) -> List[TestScenario]:
        """Search scenarios by title or description"""
        query = query.lower()
        results = []

        for scenario in self.scenarios.values():
            if (query in scenario.title.lower() or
                query in scenario.description.lower() or
                query in scenario.id.lower()):
                results.append(scenario)

        return results
