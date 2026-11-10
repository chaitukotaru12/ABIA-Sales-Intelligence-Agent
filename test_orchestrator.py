
from src.bi_agent.orchestrator import SalesIntelligenceAgent


# Initialize ABIA
agent = SalesIntelligenceAgent(
    data_path="data/sales.csv"
)

# Ask a natural-language business question
question = "Which product generated the highest revenue?"

# Run the complete agent workflow
response = agent.run(question)

# Display the final response
print("\n===== FINAL AGENT RESPONSE =====")
print(response)
