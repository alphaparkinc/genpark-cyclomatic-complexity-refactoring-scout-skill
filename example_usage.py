import sys, json
from client import CyclomaticComplexityRefactoringScout

def main():
    print("Testing CyclomaticComplexityRefactoringScout...")
    scout = CyclomaticComplexityRefactoringScout()
    res = scout.run_benchmark_complexity_scout()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["most_complex_func"] == "complex_parser"
    assert res["top_complexity"] >= 6
    print("All Cyclomatic Complexity Scout tests passed successfully!")

if __name__ == "__main__":
    main()
