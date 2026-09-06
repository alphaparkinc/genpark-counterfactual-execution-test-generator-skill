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
    BOUNDARY_STR = ["", " ", "\n", "\t", "a" * 1000, "<script>alert(1)</script>", "null", "None", "{}", "0"]
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
        elif t in ("dict", "object", "mapping"):
            return list(self.BOUNDARY_DICT)
        elif t in ("bool", "boolean"):
            return [True, False]
        else:
            return [None, "", 0]

    def synthesize_test_suite(self, signature_schema: Dict[str, str], max_tests: int = 10) -> List[Dict[str, Any]]:
        """
        Synthesize counterfactual test parameter dictionaries for a function signature.
        e.g. signature_schema = {"amount": "float", "account_id": "str"}
        """
        keys = list(signature_schema.keys())
        if not keys:
            return [{}]

        # Pick default nominal values
        nominal = {}
        for k, v in signature_schema.items():
            t = v.lower().strip()
            if t in ("int", "integer"):
                nominal[k] = 10
            elif t in ("float", "number"):
                nominal[k] = 10.5
            elif t in ("str", "string"):
                nominal[k] = "test_val"
            elif t in ("list", "array"):
                nominal[k] = ["item1"]
            elif t in ("dict", "object"):
                nominal[k] = {"key": "val"}
            elif t in ("bool", "boolean"):
                nominal[k] = True
            else:
                nominal[k] = None

        test_cases = [dict(nominal)]

        # One-at-a-time counterfactual mutation
        for k, type_name in signature_schema.items():
            mutations = self.generate_counterfactuals_for_type(type_name)
            for m in mutations[:4]:
                tc = dict(nominal)
                tc[k] = m
                test_cases.append(tc)

        # Multi-variable boundary stress
        stress_case = {}
        for k, type_name in signature_schema.items():
            candidates = self.generate_counterfactuals_for_type(type_name)
            stress_case[k] = candidates[0] if candidates else None
        test_cases.append(stress_case)

        # Deduplicate
        seen = []
        unique_tests = []
        for tc in test_cases:
            s = repr(tc)
            if s not in seen:
                seen.append(s)
                unique_tests.append(tc)

        return unique_tests[:max_tests]
