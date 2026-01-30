# experiments/sensitivity_test/run_internal_test.py

from internal_heuristic import detect_internal
from internal_samples import SAMPLES


def run():
    total = len(SAMPLES)
    wrong = 0

    for s in SAMPLES:
        text = s["text"]
        expected = s["expected_internal"]

        result = detect_internal(text)
        pred = result["is_internal"]

        ok = pred == expected
        if not ok:
            wrong += 1

        print(
            f"""
TEXT: {text}
EXPECTED is_internal: {expected}
PREDICTED: {pred}
SIGNALS: {result['signals']}
RESULT: {'OK' if ok else 'WRONG'}
-----------------------------------------
""".strip()
        )

    print("SUMMARY")
    print("-" * 40)
    print(f"Accuracy: {total - wrong}/{total}")


if __name__ == "__main__":
    run()
