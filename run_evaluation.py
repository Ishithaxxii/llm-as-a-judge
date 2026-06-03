import json
from pathlib import Path

from app.services.evaluator import LLMEvaluator


def main():
    dataset_path = Path("datasets/sample_dataset.json")

    with open(dataset_path, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    evaluator = LLMEvaluator()

    results = []

    for item in dataset:
        result = evaluator.evaluate(
            question=item["question"],
            reference_answer=item["reference_answer"],
            model_answer=item["model_answer"]
        )
        results.append(result)

    report_path = Path("reports/evaluation_report.json")
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print("Evaluation complete.")
    print(f"Saved report to: {report_path}")


if __name__ == "__main__":
    main()
