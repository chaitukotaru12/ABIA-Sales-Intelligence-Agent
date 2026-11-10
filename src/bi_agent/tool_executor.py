
class SalesToolExecutor:
    """
    Executes approved sales analysis tools.
    """

    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.tool_registry = {
            "get_overview": self.analyzer.get_overview,
            "revenue_by_product": self.analyzer.revenue_by_product,
            "revenue_by_region": self.analyzer.revenue_by_region,
            "monthly_revenue": self.analyzer.monthly_revenue,
            "get_data_quality": self.analyzer.get_data_quality
        }

    def execute_plan(self, plan):

        if not isinstance(plan, dict):
            raise ValueError("Invalid analysis plan.")

        tools = plan.get("tools")

        if not isinstance(tools, list) or not tools:
            raise ValueError("Plan must contain approved tools.")

        results = {}

        for tool_name in tools:

            if tool_name not in self.tool_registry:
                raise ValueError(
                    f"Unauthorized tool: {tool_name}"
                )

            tool_function = self.tool_registry[tool_name]

            result = tool_function()

            # Convert Pandas Series into dictionaries
            if hasattr(result, "to_dict"):
                result = result.to_dict()

            results[tool_name] = result

        return results
