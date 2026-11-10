
from src.bi_agent.report_generator import SalesReportGenerator


generator = SalesReportGenerator()

# Simulated results from the approved analysis
results = {
    "revenue_by_product": {
        "Laptop": 480000,
        "Mobile": 360000,
        "Tablet": 150000
    }
}

# Simulated successful critic review
review = {
    "approved": True,
    "issues": []
}

question = "Which product generated the highest revenue?"

# Generate report
report = generator.generate_report(
    question=question,
    results=results,
    review=review
)

print("\n===== GENERATED SALES REPORT =====")
print(report)
