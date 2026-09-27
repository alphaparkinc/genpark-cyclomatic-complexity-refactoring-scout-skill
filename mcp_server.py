import sys, json
from client import CyclomaticComplexityRefactoringScout

def main():
    scout = CyclomaticComplexityRefactoringScout()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(scout.run_benchmark_complexity_scout(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "calculate_cyclomatic_complexity", "description": "Compute McCabe complexity per function using AST node branching."},
                        {"name": "run_benchmark_complexity_scout", "description": "Run complexity benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "calculate_cyclomatic_complexity":
                    out = scout.calculate_cyclomatic_complexity(args.get("python_code", ""))
                elif tname == "run_benchmark_complexity_scout":
                    out = scout.run_benchmark_complexity_scout()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
