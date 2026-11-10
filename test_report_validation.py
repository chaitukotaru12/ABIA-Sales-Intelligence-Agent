
from src.bi_agent.report_generator import SalesReportGenerator


generator = SalesReportGenerator()


def run_test(test_name, results, review, should_pass):

    print(f"\n===== TEST: {test_name} =====")

    try:
        report = generator.generate_report(
            question="Which product generated the highest revenue?",
            results=results,
            review=review
        )

        if should_pass:
            print("SUCCESS: Valid report accepted.")
            print(report)
        else:
            print("ERROR: Incorrect report was accepted!")
            print(report)

    except ValueError as error:

        if should_pass:
            print("ERROR: Valid report was rejected.")
            print("Reason:", error)
        else:
            print("SUCCESS: Incorrect report rejected.")
            print("Reason:", error)


# TEST 1: Incorrect conclusion must be rejected
false_results = {
    "revenue_by_product": {
        "Laptop": 480000,
        "Mobile": 360000,
        "Tablet": 150000
    }
}

false_review = {
    "approved": True,
    "issues": [],
    "findings": {
        "highest_revenue_products": ["Mobile"],
        "highest_revenue": 360000
    }
}

run_test(
    "FALSE BUSINESS CONCLUSION",
    false_results,
    false_review,
    should_pass=False
)


# TEST 2: Correct conclusion must be accepted
valid_review = {
    "approved": True,
    "issues": [],
    "findings": {
        "highest_revenue_products": ["Laptop"],
        "highest_revenue": 480000
    }
}

run_test(
    "VALID BUSINESS CONCLUSION",
    false_results,
    valid_review,
    should_pass=True
)


# TEST 3: Multiple products tied for highest revenue
tie_results = {
    "revenue_by_product": {
        "Laptop": 480000,
        "Mobile": 480000,
        "Tablet": 150000
    }
}

tie_review = {
    "approved": True,
    "issues": [],
    "findings": {
        "highest_revenue_products": ["Laptop", "Mobile"],
        "highest_revenue": 480000
    }
}

run_test(
    "TIED HIGHEST-REVENUE PRODUCTS",
    tie_results,
    tie_review,
    should_pass=True
)
