
from src.bi_agent.critic import SalesAnalysisCritic

critic = SalesAnalysisCritic()

plan = {
    "objective": "Identify the highest revenue product",
    "tools": ["revenue_by_product"],
    "steps": ["Compare product revenues"]
}

# Test 1: Valid results
valid_results = {
    "revenue_by_product": {
        "Laptop": 480000,
        "Mobile": 360000,
        "Tablet": 150000
    }
}

# Test 2: Invalid negative revenue
invalid_results = {
    "revenue_by_product": {
        "Laptop": -480000,
        "Mobile": 360000,
        "Tablet": 150000
    }
}

# Test 3: Missing tool results
missing_results = {}

print("\n===== TEST 1: VALID RESULTS =====")
print(critic.review("Which product leads?", plan, valid_results))

print("\n===== TEST 2: INVALID REVENUE =====")
print(critic.review("Which product leads?", plan, invalid_results))

print("\n===== TEST 3: MISSING RESULTS =====")
print(critic.review("Which product leads?", plan, missing_results))
