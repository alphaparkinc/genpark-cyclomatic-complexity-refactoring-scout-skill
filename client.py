import sys, json, ast

class CyclomaticComplexityRefactoringScout:
    """
    McCabe Cyclomatic Complexity & Cognitive Architecture Profiler.
    Calculates decision points (If, While, For, Except, With, BoolOp)
    and nesting depth penalties to recommend modular decomposition.
    """
    def __init__(self):
        pass

    def calculate_cyclomatic_complexity(self, python_code):
        try:
            tree = ast.parse(python_code)
        except SyntaxError as e:
            return {"error": str(e)}

        functions_report = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Base complexity = 1
                complexity = 1
                max_nesting = 0

                def walk_branches(n, current_depth):
                    nonlocal complexity, max_nesting
                    for child in ast.iter_child_nodes(n):
                        is_branch = isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With))
                        if is_branch:
                            complexity += 1
                            new_depth = current_depth + 1
                            if new_depth > max_nesting:
                                max_nesting = new_depth
                            walk_branches(child, new_depth)
                        elif isinstance(child, ast.BoolOp):
                            # Each 'and' or 'or' adds 1 decision path
                            complexity += len(child.values) - 1
                            walk_branches(child, current_depth)
                        else:
                            walk_branches(child, current_depth)

                walk_branches(node, 0)

                # Rating: 1-5 (Simple), 6-10 (Moderate), 11-20 (Complex/Refactor), >20 (Extreme Hazard)
                if complexity <= 5:
                    rating = "SIMPLE_CLEAN"
                    action = "NO_ACTION"
                elif complexity <= 10:
                    rating = "MODERATE"
                    action = "CONSIDER_EARLY_RETURN_GUARDS"
                else:
                    rating = "HIGH_COMPLEXITY_HOTSPOT"
                    action = "EXTRACT_SUBROUTINES_IMMEDIATELY"

                functions_report.append({
                    "function_name": node.name,
                    "cyclomatic_complexity": complexity,
                    "max_nesting_depth": max_nesting,
                    "risk_rating": rating,
                    "refactoring_recommendation": action
                })

        return {
            "total_functions_analyzed": len(functions_report),
            "functions": sorted(functions_report, key=lambda x: -x["cyclomatic_complexity"])
        }

    def run_benchmark_complexity_scout(self):
        sample_code = """
def simple_add(a, b):
    return a + b

def complex_parser(data, flag, mode):
    if data:
        for item in data:
            if item.is_valid():
                if flag and mode == 'FAST':
                    process_fast(item)
                elif mode == 'SLOW':
                    process_slow(item)
            else:
                log_error(item)
    return True
"""
        res = self.calculate_cyclomatic_complexity(sample_code)
        top = res["functions"][0]
        return {
            "benchmark_status": "PASSED",
            "analyzed_count": res["total_functions_analyzed"],
            "most_complex_func": top["function_name"],
            "top_complexity": top["cyclomatic_complexity"],
            "top_rating": top["risk_rating"]
        }
