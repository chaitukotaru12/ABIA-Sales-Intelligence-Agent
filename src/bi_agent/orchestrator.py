
from src.bi_agent.data_analyzer import SalesAnalyzer
from src.bi_agent.analysis_planner import SalesAnalysisPlanner
from src.bi_agent.tool_executor import SalesToolExecutor
from src.bi_agent.critic import SalesAnalysisCritic
from src.bi_agent.report_generator import SalesReportGenerator


class SalesIntelligenceAgent:
    """
    Coordinates the complete ABIA workflow.
    """

    def __init__(self, data_path, model="qwen3:4b"):

        self.analyzer = SalesAnalyzer(data_path)
        self.analyzer.load_data()

        self.planner = SalesAnalysisPlanner(model=model)
        self.executor = SalesToolExecutor(self.analyzer)
        self.critic = SalesAnalysisCritic()
        self.report_generator = SalesReportGenerator()

    def run(self, question):

        if not isinstance(question, str) or not question.strip():
            raise ValueError("Please provide a valid business question.")

        print("\n===== ABIA: SALES INTELLIGENCE AGENT =====")
        print(f"Question: {question}")

        # Step 1: Planning
        plan = self.planner.create_plan(question)

        print("\n===== ANALYSIS PLAN =====")
        print(plan)

        # Step 2: Execution
        results = self.executor.execute_plan(plan)

        print("\n===== ANALYSIS RESULTS =====")
        print(results)

        # Step 3: Critic review
        review = self.critic.review(
            question=question,
            plan=plan,
            results=results
        )

        print("\n===== CRITIC REVIEW =====")
        print(review)

        if not review["approved"]:
            raise ValueError(
                f"Analysis rejected: {review['issues']}"
            )

        print("\n===== ANALYSIS APPROVED =====")

        # Step 4: Report generation
        report = self.report_generator.generate_report(
            question=question,
            results=results,
            review=review
        )

        print("\n===== FINAL BUSINESS REPORT =====")
        print(report)

        return {
            "question": question,
            "plan": plan,
            "results": results,
            "review": review,
            "report": report
        }
