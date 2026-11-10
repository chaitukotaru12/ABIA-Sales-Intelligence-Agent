
from src.bi_agent.data_analyzer import SalesAnalyzer

# Initialize the analyzer
analyzer = SalesAnalyzer("data/sales.csv")

# Load sales data
df = analyzer.load_data()

print("\n===== DATA PREVIEW =====")
print(df.head())

print("\n===== BUSINESS OVERVIEW =====")
print(analyzer.get_overview())

print("\n===== PRODUCT PERFORMANCE =====")
print(analyzer.revenue_by_product())

print("\n===== REGIONAL PERFORMANCE =====")
print(analyzer.revenue_by_region())

print("\n===== MONTHLY REVENUE =====")
print(analyzer.monthly_revenue())

print("\n===== DATA QUALITY =====")
print(analyzer.get_data_quality())
