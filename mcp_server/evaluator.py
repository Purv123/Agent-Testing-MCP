"""
Test Evaluator

Integrates with DeepEval and custom metrics to evaluate AI agent solutions.
Assesses correctness, code quality, relevance, and completeness.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import DeepEval - graceful degradation if not available
try:
    from deepeval.metrics import (
        AnswerRelevancyMetric,
        FaithfulnessMetric,
        ContextualRelevancyMetric,
    )
    from deepeval.test_case import LLMTestCase
    DEEPEVAL_AVAILABLE = True
except ImportError:
    logger.warning("DeepEval not available. Using basic evaluation only.")
    DEEPEVAL_AVAILABLE = False


class TestEvaluator:
    """Evaluates AI agent solutions using multiple criteria"""

    def __init__(self):
        self.deepeval_enabled = DEEPEVAL_AVAILABLE
        logger.info(f"Test evaluator initialized (DeepEval: {self.deepeval_enabled})")

    async def evaluate(
        self,
        scenario: Any,  # TestScenario
        code: str,
        execution_result: Dict[str, Any],
        explanation: str = ""
    ) -> Dict[str, Any]:
        """
        Comprehensive evaluation of a solution

        Args:
            scenario: Test scenario
            code: Submitted code
            execution_result: Execution results
            explanation: Agent's explanation

        Returns:
            Evaluation results with scores and feedback
        """
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "scenario_id": scenario.id,
            "passed": False,
            "status": "failed",
            "overall_score": 0.0,
            "metrics": {},
            "feedback": [],
            "summary": ""
        }

        # 1. Correctness - Based on test execution
        correctness = self._evaluate_correctness(execution_result)
        evaluation["metrics"]["correctness"] = correctness

        # 2. Code Quality
        quality = self._evaluate_code_quality(code, scenario.language)
        evaluation["metrics"]["quality"] = quality

        # 3. Completeness
        completeness = self._evaluate_completeness(
            code, scenario.requirements, execution_result
        )
        evaluation["metrics"]["completeness"] = completeness

        # 4. Relevance - Does it address the task?
        relevance = self._evaluate_relevance(code, scenario, explanation)
        evaluation["metrics"]["relevance"] = relevance

        # 5. DeepEval metrics (if available and applicable)
        if self.deepeval_enabled and explanation:
            deepeval_metrics = await self._evaluate_deepeval(
                scenario, code, explanation
            )
            evaluation["metrics"]["deepeval"] = deepeval_metrics

        # Calculate overall score
        weights = scenario.evaluation_metrics.get("weights", {
            "correctness": 0.4,
            "quality": 0.2,
            "completeness": 0.2,
            "relevance": 0.2
        })

        overall_score = (
            correctness["score"] * weights.get("correctness", 0.4) +
            quality["score"] * weights.get("quality", 0.2) +
            completeness["score"] * weights.get("completeness", 0.2) +
            relevance["score"] * weights.get("relevance", 0.2)
        )

        evaluation["overall_score"] = round(overall_score, 2)

        # Determine pass/fail
        threshold = scenario.evaluation_metrics.get("pass_threshold", 0.7)
        evaluation["passed"] = overall_score >= threshold
        evaluation["status"] = "passed" if evaluation["passed"] else "failed"

        # Generate feedback
        evaluation["feedback"] = self._generate_feedback(evaluation["metrics"])
        evaluation["summary"] = self._generate_summary(evaluation)

        return evaluation

    def _evaluate_correctness(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate correctness based on test execution"""
        if not execution_result.get("success", False):
            return {
                "score": 0.0,
                "details": "Code execution failed",
                "passed_tests": 0,
                "total_tests": 0
            }

        test_results = execution_result.get("test_results", [])
        if not test_results:
            # If no tests, check if code ran without errors
            return {
                "score": 0.5 if execution_result.get("success") else 0.0,
                "details": "No test cases to validate",
                "passed_tests": 0,
                "total_tests": 0
            }

        passed = sum(1 for t in test_results if t.get("passed", False))
        total = len(test_results)
        score = passed / total if total > 0 else 0.0

        return {
            "score": score,
            "details": f"Passed {passed}/{total} test cases",
            "passed_tests": passed,
            "total_tests": total,
            "test_results": test_results
        }

    def _evaluate_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """Evaluate code quality using static analysis"""
        issues = []
        score = 1.0

        # Basic quality checks
        lines = code.split('\n')

        # Check for reasonable length
        if len(code.strip()) < 10:
            issues.append("Code is too short")
            score -= 0.3

        # Check for comments/documentation
        comment_chars = {'python': '#', 'javascript': '//', 'typescript': '//'}
        comment_char = comment_chars.get(language, '#')
        has_comments = any(comment_char in line for line in lines)

        if not has_comments and len(lines) > 10:
            issues.append("No comments or documentation")
            score -= 0.1

        # Check for very long lines
        long_lines = [i for i, line in enumerate(lines) if len(line) > 120]
        if long_lines:
            issues.append(f"Found {len(long_lines)} lines exceeding 120 characters")
            score -= 0.1

        # Check for proper indentation (basic)
        if language == "python":
            inconsistent_indent = self._check_python_indentation(lines)
            if inconsistent_indent:
                issues.append("Inconsistent indentation detected")
                score -= 0.2

        # Check for error handling
        error_keywords = ['try', 'except', 'catch', 'error', 'Error']
        has_error_handling = any(keyword in code for keyword in error_keywords)

        if len(lines) > 20 and not has_error_handling:
            issues.append("No error handling detected in longer code")
            score -= 0.1

        score = max(0.0, min(1.0, score))

        return {
            "score": round(score, 2),
            "details": "Code quality assessment",
            "issues": issues,
            "has_comments": has_comments,
            "has_error_handling": has_error_handling,
            "lines_of_code": len(lines)
        }

    def _check_python_indentation(self, lines: List[str]) -> bool:
        """Check for inconsistent Python indentation"""
        indent_sizes = set()
        for line in lines:
            if line.strip() and line[0] == ' ':
                # Count leading spaces
                spaces = len(line) - len(line.lstrip(' '))
                if spaces > 0:
                    indent_sizes.add(spaces)

        # If we have both 2-space and 4-space (or other combinations), it's inconsistent
        return len(indent_sizes) > 1

    def _evaluate_completeness(
        self,
        code: str,
        requirements: List[str],
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate if solution is complete"""
        score = 1.0
        missing = []

        # Check if code addresses requirements
        code_lower = code.lower()

        for req in requirements:
            # Simple keyword matching - more sophisticated NLP could be added
            req_keywords = req.lower().split()
            key_words_found = sum(1 for kw in req_keywords if kw in code_lower)

            if key_words_found < len(req_keywords) * 0.3:  # At least 30% keywords
                missing.append(req)
                score -= 0.2

        # Check if execution was successful
        if not execution_result.get("success", False):
            score -= 0.3

        score = max(0.0, min(1.0, score))

        return {
            "score": round(score, 2),
            "details": "Completeness assessment",
            "missing_requirements": missing,
            "total_requirements": len(requirements)
        }

    def _evaluate_relevance(
        self,
        code: str,
        scenario: Any,
        explanation: str
    ) -> Dict[str, Any]:
        """Evaluate if solution is relevant to the task"""
        score = 1.0

        # Check if code appears to address the scenario
        scenario_keywords = (
            scenario.title.lower().split() +
            scenario.description.lower().split()
        )

        code_lower = code.lower()
        explanation_lower = explanation.lower() if explanation else ""

        # Count keyword matches
        matches_in_code = sum(1 for kw in scenario_keywords if kw in code_lower)
        matches_in_explanation = sum(1 for kw in scenario_keywords if kw in explanation_lower)

        total_keywords = len(set(scenario_keywords))
        if total_keywords > 0:
            relevance_ratio = (matches_in_code + matches_in_explanation) / (total_keywords * 2)
            score = min(1.0, relevance_ratio * 1.5)  # Scale up a bit

        return {
            "score": round(score, 2),
            "details": "Relevance to task",
            "keyword_matches": matches_in_code + matches_in_explanation,
            "total_keywords": total_keywords
        }

    async def _evaluate_deepeval(
        self,
        scenario: Any,
        code: str,
        explanation: str
    ) -> Dict[str, Any]:
        """Evaluate using DeepEval metrics"""
        if not self.deepeval_enabled:
            return {"available": False}

        try:
            # Create test case for DeepEval
            test_case = LLMTestCase(
                input=scenario.description,
                actual_output=f"{explanation}\n\n```{scenario.language}\n{code}\n```",
                expected_output=scenario.context,
                context=[scenario.description, *scenario.requirements]
            )

            results = {}

            # Run relevancy metric
            try:
                relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
                relevancy_metric.measure(test_case)
                results["relevancy"] = {
                    "score": relevancy_metric.score,
                    "threshold": relevancy_metric.threshold,
                    "passed": relevancy_metric.score >= relevancy_metric.threshold
                }
            except Exception as e:
                logger.warning(f"DeepEval relevancy metric failed: {e}")

            return results

        except Exception as e:
            logger.error(f"DeepEval evaluation failed: {e}")
            return {"available": True, "error": str(e)}

    def _generate_feedback(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate human-readable feedback"""
        feedback = []

        # Correctness feedback
        correctness = metrics.get("correctness", {})
        if correctness.get("score", 0) == 1.0:
            feedback.append("✓ All test cases passed successfully")
        elif correctness.get("score", 0) > 0:
            feedback.append(
                f"⚠ Partial success: {correctness.get('details', 'Some tests failed')}"
            )
        else:
            feedback.append("✗ Test cases failed or code did not execute")

        # Quality feedback
        quality = metrics.get("quality", {})
        if quality.get("issues"):
            feedback.append(f"Code quality issues: {', '.join(quality['issues'])}")
        elif quality.get("score", 0) > 0.8:
            feedback.append("✓ Good code quality")

        # Completeness feedback
        completeness = metrics.get("completeness", {})
        if completeness.get("missing_requirements"):
            feedback.append(
                f"Missing requirements: {', '.join(completeness['missing_requirements'][:3])}"
            )
        elif completeness.get("score", 0) > 0.8:
            feedback.append("✓ Solution appears complete")

        return feedback

    def _generate_summary(self, evaluation: Dict[str, Any]) -> str:
        """Generate evaluation summary"""
        status = evaluation["status"]
        score = evaluation["overall_score"]

        if status == "passed":
            return f"✓ Solution PASSED with score {score:.2f}. Well done!"
        else:
            return f"✗ Solution FAILED with score {score:.2f}. Review feedback and try again."
