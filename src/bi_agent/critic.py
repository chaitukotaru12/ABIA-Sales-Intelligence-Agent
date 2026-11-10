
import math


class SalesAnalysisCritic:
    """
    Independently validates sales analysis evidence
    and derives verified business findings.
    """

    def review(self, question, plan, results):

        issues = []
        findings = {}

        # Check 1: Validate the question
        if not isinstance(question, str) or not question.strip():
            issues.append("Invalid business question.")

        # Check 2: Validate the analysis plan
        if not isinstance(plan, dict):
            return {
                "approved": False,
                "issues": ["Invalid analysis plan."],
                "findings": {}
            }

        tools = plan.get("tools")

        if not isinstance(tools, list) or not tools:
            issues.append("No valid analysis tools were selected.")
            tools = []

        # Check 3: Validate execution results
        if not isinstance(results, dict) or not results:
            issues.append("No analysis results were returned.")
            results = {}

        # Check 4: Verify every planned tool returned results
        for tool_name in tools:

            if not isinstance(tool_name, str):
                issues.append("Invalid tool name in analysis plan.")
                continue

            if tool_name not in results:
                issues.append(
                    f"Missing results for tool: {tool_name}"
                )

        # Check 5: Validate product revenue evidence
        if "revenue_by_product" in results:

            product_data = results["revenue_by_product"]

            if not isinstance(product_data, dict) or not product_data:
                issues.append("Product revenue data is invalid.")

            else:

                valid_product_data = {}

                for product, revenue in product_data.items():

                    if (
                        not isinstance(product, str)
                        or not product.strip()
                    ):
                        issues.append("Invalid product name.")
                        continue

                    if (
                        isinstance(revenue, bool)
                        or not isinstance(revenue, (int, float))
                    ):
                        issues.append(
                            f"Invalid revenue value for {product}."
                        )
                        continue

                    if not math.isfinite(revenue):
                        issues.append(
                            f"Non-finite revenue found for {product}."
                        )
                        continue

                    if revenue < 0:
                        issues.append(
                            f"Negative revenue found for {product}."
                        )
                        continue

                    valid_product_data[product] = revenue

                # Independently calculate the highest-revenue product
                if (
                    valid_product_data
                    and not any(
                        issue.startswith(
                            ("Invalid revenue", "Negative revenue",
                             "Non-finite revenue", "Invalid product")
                        )
                        for issue in issues
                    )
                ):

                    highest_revenue = max(
                        valid_product_data.values()
                    )

                    top_products = [
                        product
                        for product, revenue in valid_product_data.items()
                        if revenue == highest_revenue
                    ]

                    findings["highest_revenue_products"] = top_products
                    findings["highest_revenue"] = highest_revenue

        # Check 6: Ensure product questions have product evidence
        if (
            isinstance(question, str)
            and "product" in question.lower()
            and any(
                word in question.lower()
                for word in ["highest", "top", "best", "most"]
            )
        ):

            if "revenue_by_product" not in results:
                issues.append(
                    "Product revenue evidence is required "
                    "to answer this question."
                )

            elif not findings.get("highest_revenue_products"):
                issues.append(
                    "Unable to establish the highest-revenue product."
                )

        approved = len(issues) == 0

        return {
            "approved": approved,
            "issues": issues,
            "findings": findings
        }
