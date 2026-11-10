
class SalesReportGenerator:
    """
    Generates business reports using critic-approved findings.
    Independently validates product revenue conclusions.
    """

    def generate_report(self, question, results, review):

        # Check critic approval
        if not isinstance(review, dict) or not review.get("approved", False):
            raise ValueError(
                "Cannot generate a report from unapproved analysis."
            )

        if not isinstance(results, dict) or not results:
            raise ValueError("No analysis results available.")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("A valid business question is required.")

        findings = review.get("findings", {})

        if not isinstance(findings, dict):
            raise ValueError("Invalid critic findings.")

        report = []

        report.append("=" * 60)
        report.append("ABIA - SALES INTELLIGENCE REPORT")
        report.append("=" * 60)

        report.append(f"\nBusiness Question:\n{question}")

        # Executive summary
        report.append("\nEXECUTIVE SUMMARY")
        report.append("-" * 60)

        if "revenue_by_product" in results:

            product_data = results["revenue_by_product"]

            if not isinstance(product_data, dict) or not product_data:
                raise ValueError("Invalid product revenue data.")

            # Validate product revenue values
            for product, revenue in product_data.items():
                if (
                    not isinstance(product, str)
                    or not product.strip()
                    or isinstance(revenue, bool)
                    or not isinstance(revenue, (int, float))
                    or not isinstance(revenue, (int, float))
                    or revenue < 0
                    or not __import__("math").isfinite(revenue)
                ):
                    raise ValueError(
                        f"Invalid product revenue data for: {product}"
                    )

            # Retrieve critic findings
            top_products = findings.get("highest_revenue_products")
            highest_revenue = findings.get("highest_revenue")

            if not isinstance(top_products, list) or not top_products:
                raise ValueError(
                    "Critic did not provide verified product findings."
                )

            if (
                isinstance(highest_revenue, bool)
                or not isinstance(highest_revenue, (int, float))
            ):
                raise ValueError("Invalid critic revenue finding.")

            # Independently calculate the actual maximum revenue
            actual_highest_revenue = max(product_data.values())

            actual_top_products = [
                product
                for product, revenue in product_data.items()
                if revenue == actual_highest_revenue
            ]

            # Compare critic findings against actual evidence
            if set(top_products) != set(actual_top_products):
                raise ValueError(
                    "Critic finding does not identify the actual "
                    "highest-revenue product."
                )

            if highest_revenue != actual_highest_revenue:
                raise ValueError(
                    "Critic finding does not match the actual "
                    "highest revenue."
                )

            # Generate executive summary
            if len(actual_top_products) == 1:
                report.append(
                    f"{actual_top_products[0]} generated the highest "
                    f"revenue of {actual_highest_revenue:,.2f}."
                )
            else:
                report.append(
                    f"{', '.join(actual_top_products)} share the highest "
                    f"revenue of {actual_highest_revenue:,.2f}."
                )

            # Product revenue breakdown
            report.append("\nREVENUE BY PRODUCT")
            report.append("-" * 60)

            for product, revenue in sorted(
                product_data.items(),
                key=lambda item: item[1],
                reverse=True
            ):
                report.append(f"{product}: {revenue:,.2f}")

        # Regional analysis
        if "revenue_by_region" in results:

            region_data = results["revenue_by_region"]

            if not isinstance(region_data, dict):
                raise ValueError("Invalid regional revenue data.")

            report.append("\nREVENUE BY REGION")
            report.append("-" * 60)

            for region, revenue in region_data.items():
                report.append(f"{region}: {revenue:,.2f}")

        # Sales overview
        if "get_overview" in results:

            overview = results["get_overview"]

            if not isinstance(overview, dict):
                raise ValueError("Invalid sales overview.")

            report.append("\nSALES OVERVIEW")
            report.append("-" * 60)

            for metric, value in overview.items():
                report.append(f"{metric}: {value}")

        # Monthly revenue
        if "monthly_revenue" in results:

            monthly_data = results["monthly_revenue"]

            if not isinstance(monthly_data, dict):
                raise ValueError("Invalid monthly revenue data.")

            report.append("\nMONTHLY REVENUE")
            report.append("-" * 60)

            for month, revenue in monthly_data.items():
                report.append(f"{month}: {revenue:,.2f}")

        # Data quality
        if "get_data_quality" in results:

            quality = results["get_data_quality"]

            if not isinstance(quality, dict):
                raise ValueError("Invalid data quality results.")

            report.append("\nDATA QUALITY")
            report.append("-" * 60)

            for metric, value in quality.items():
                report.append(f"{metric}: {value}")

        # Validation status
        report.append("\nVALIDATION STATUS")
        report.append("-" * 60)
        report.append("Analysis approved by ABIA Critic.")
        report.append(
            "Product revenue conclusions independently checked "
            "against execution results."
        )

        report.append("\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)

        return "\n".join(report)
