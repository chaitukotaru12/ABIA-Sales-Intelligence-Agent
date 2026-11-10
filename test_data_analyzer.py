
import unittest

from src.bi_agent.data_analyzer import SalesAnalyzer


class TestSalesAnalyzer(unittest.TestCase):

    def setUp(self):
        # Initialize the analyzer before each test
        self.analyzer = SalesAnalyzer("data/sales.csv")
        self.analyzer.load_data()

    def test_total_revenue(self):
        overview = self.analyzer.get_overview()
        self.assertEqual(overview["total_revenue"], 990000)

    def test_total_quantity(self):
        overview = self.analyzer.get_overview()
        self.assertEqual(overview["total_quantity"], 42)

    def test_total_transactions(self):
        overview = self.analyzer.get_overview()
        self.assertEqual(overview["total_transactions"], 15)

    def test_average_transaction_value(self):
        overview = self.analyzer.get_overview()
        self.assertEqual(
            overview["average_transaction_value"], 66000
        )

    def test_product_revenue(self):
        result = self.analyzer.revenue_by_product()

        self.assertEqual(result["Laptop"], 480000)
        self.assertEqual(result["Mobile"], 360000)
        self.assertEqual(result["Tablet"], 150000)

    def test_region_revenue(self):
        result = self.analyzer.revenue_by_region()

        self.assertEqual(result["South"], 450000)
        self.assertEqual(result["East"], 240000)
        self.assertEqual(result["North"], 150000)
        self.assertEqual(result["West"], 150000)

    def test_monthly_revenue(self):
        result = self.analyzer.monthly_revenue()

        self.assertEqual(result.iloc[0], 420000)
        self.assertEqual(result.iloc[1], 360000)
        self.assertEqual(result.iloc[2], 210000)

    def test_data_quality(self):
        quality = self.analyzer.get_data_quality()

        self.assertEqual(quality["total_records"], 15)
        self.assertEqual(quality["missing_values"], 0)
        self.assertEqual(quality["invalid_rows_removed"], 0)
        self.assertEqual(quality["duplicate_rows"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
