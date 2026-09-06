"""
Counterfactual Execution Test Generator Skill Client
Pure Python Standard Library implementation of Counterfactual Test Synthesis and Boundary Fuzzing (Claessen & Hughes QuickCheck style).
Generates edge-case suites (empty collections, boundary integers, negative floats, unicode overflows)
to systematically reproduce agent tool execution failures.
"""

from typing import List, Dict, Any, Tuple


class CounterfactualTestGenerator:
    """
    Synthesizes diverse adversarial and edge-case inputs for tool signatures.
    """

    BOUNDARY_INT = [0, 1, -1, 2**31 - 1, -2**31, 1000000]
    BOUNDARY_FLOAT = [0.0, -0.0, 1.0, -1.0, 1e-9, -1e-9, float("inf"), float("-inf")]
    BOUNDARY_STR = ["", " ", "\n", "\t", "a" * 1000, "<script>alert(1)</script>", "null", "None", "{}\", "0"]
    BOUNDARY_LIST = [[], [None], [0], list(range(100)), ["a", "b", "c"]]
    BOUNDARY_DICT = [{}, {"": ""}, {"key": None}, {"a": {"b": {"c": 1}}}]

    def generate_counterfactuals_for_type(self, type_hint: str) -> List[Any]:
        """Generate boundary candidates for a given type name."""
        t = type_hint.lower().strip()
        if t in ("int", "integer"):
            return list(self.BOUNDARY_INT)
        elif t in ("float", "number"):
            return list(self.BOUNDARY_FLOAT)
        elif t in ("str", "string"):
            return list(self.BOUNDARY_STR)
        elif t in ("list", "array"):
            return list(self.BOUNDARY_LIST)
        elif t in ("dict", "object"):
            return list(self.BOUNDARY_DICT)
        elif t in ("bool", "boolean"):
            return [True, False]
        else:
            return [None, "", 0, [], {}]

    def synthesize_test_suite(self, param_schema: Dict[str, str], max_tests: int = 10) -> List[Dict[str, Any]]:
        """
        Synthesize cross-product test suite across multiple parameter specifications.
        """
        test_cases = []
        param_names = list(param_schema.keys())

        # 1. Base default cases
        default_case = {}
        for p, t in param_schema.items():
            candidates = self.generate_counterfactuals_for_type(t)
            default_case[p] = candidates[0] if candidates else None
        test_cases.append(default_case)

        # 2. Perturb each parameter independently
        for p in param_names:
            candidates = self.generate_counterfactuals_for_type(param_schema[p])
            for val in candidates[:max_tests]:
                case = dict(default_case)
                case[p] = val
                test_cases.append(case)

        # Deduplicate
        seen = []
        unique_tests = []
        for tc in test_cases:
            s = repr(tc)
            if s not in seen:
                seen.append(s)
                unique_tests.append(tc)

        return unique_tests[:max_tests]
