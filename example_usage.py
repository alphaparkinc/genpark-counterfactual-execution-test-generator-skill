"""
Example usage of Counterfactual Execution Test Generator Skill.
"""

from client import CounterfactualTestGenerator


def main():
    print("=== Counterfactual Execution Test Generator Demonstration ===")
    generator = CounterfactualTestGenerator()

    # Tool signature schema: process_payment(amount: float, user_id: str, items: list)
    schema = {
        "amount": "float",
        "user_id": "str",
        "items": "list"
    }

    print("Target Schema:", schema)
    suite = generator.synthesize_test_suite(schema, max_tests=8)

    print(f"\nSynthesized {len(suite)} Counterfactual Edge-Case Test Inputs:")
    for idx, tc in enumerate(suite, 1):
        print(f"  Test Case #{idx}: {tc}")


if __name__ == "__main__":
    main()
