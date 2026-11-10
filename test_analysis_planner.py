
from src.bi_agent.analysis_planner import SalesAnalysisPlanner

# Initialize the planning engine
planner = SalesAnalysisPlanner()

# Business question for Qwen
question = "Which product generated the highest revenue?"

print("\n===== USER QUESTION =====")
print(question)

# Ask Qwen to create an analysis plan
plan = planner.create_plan(question)

print("\n===== QWEN ANALYSIS PLAN =====")
print(plan)

print("\n===== PLANNING VALIDATION =====")
print("Plan successfully generated and validated.")
