
from pathlib import Path

import pandas as pd


class SalesAnalyzer:
    """
    Loads and standardizes sales CSV files.

    Supports common column-name variations and can calculate
    revenue from quantity multiplied by unit price.

    Standard internal columns:
        date, product, region, quantity, revenue
    """

    COLUMN_ALIASES = {
        "date": [
            "date",
            "order date",
            "invoicedate",
            "invoice date",
            "transaction date",
            "sales date",
            "purchase date",
        ],
        "product": [
            "product",
            "product name",
            "productname",
            "description",
            "item",
            "item name",
            "stock description",
        ],
        "region": [
            "region",
            "country",
            "market",
            "territory",
            "state",
            "sales region",
        ],
        "quantity": [
            "quantity",
            "qty",
            "units sold",
            "unit sold",
            "units",
            "order quantity",
        ],
        "revenue": [
            "revenue",
            "sales",
            "amount",
            "total sales",
            "total revenue",
            "sales amount",
            "line total",
            "total amount",
        ],
        "unit_price": [
            "unit price",
            "unitprice",
            "price per unit",
            "price",
            "unit cost",
        ],
    }

    def __init__(self, data_path):
        self.data_path = Path(data_path)

        self.raw_df = None
        self.df = None
        self.quality_report = {}

        self.column_mapping = {}
        self.revenue_calculation = None

    @staticmethod
    def _normalize_column_name(column):
        """Normalize column names for reliable matching."""

        return (
            str(column)
            .strip()
            .lower()
            .replace("_", " ")
            .replace("-", " ")
            .replace(".", " ")
        ).strip()

    def _find_column(self, normalized_columns, aliases):
        """Find the first matching source column."""

        alias_set = {
            self._normalize_column_name(alias)
            for alias in aliases
        }

        for original, normalized in normalized_columns.items():
            if normalized in alias_set:
                return original

        return None

    def _detect_columns(self, dataframe):
        """Automatically map source columns to ABIA fields."""

        normalized_columns = {
            column: self._normalize_column_name(column)
            for column in dataframe.columns
        }

        mapping = {}

        for standard_name, aliases in self.COLUMN_ALIASES.items():
            mapping[standard_name] = self._find_column(
                normalized_columns,
                aliases
            )

        required_fields = [
            "date",
            "product",
            "region",
            "quantity",
        ]

        missing_fields = [
            field
            for field in required_fields
            if mapping[field] is None
        ]

        # Revenue can either be supplied directly or calculated
        # using quantity multiplied by unit price.
        if mapping["revenue"] is None and mapping["unit_price"] is None:
            missing_fields.append("revenue or unit price")

        if missing_fields:
            available = ", ".join(str(c) for c in dataframe.columns)

            raise ValueError(
                "ABIA could not identify these required fields: "
                + ", ".join(missing_fields)
                + ". Available CSV columns: "
                + available
                + ". Please rename the columns or provide a compatible CSV."
            )

        return mapping

    def load_data(self):
        """Load, standardize and validate the sales dataset."""

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.data_path}"
            )

        # Read CSV, supporting common text encodings.
        try:
            dataframe = pd.read_csv(self.data_path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            dataframe = pd.read_csv(self.data_path, encoding="latin1")

        if dataframe.empty:
            raise ValueError("The uploaded CSV file is empty.")

        if len(dataframe.columns) == 0:
            raise ValueError("The CSV file contains no columns.")

        self.raw_df = dataframe.copy()

        # Detect source column names.
        self.column_mapping = self._detect_columns(dataframe)

        # Build the standard ABIA dataframe.
        standardized = pd.DataFrame(index=dataframe.index)

        for field in ["date", "product", "region", "quantity"]:
            source_column = self.column_mapping[field]
            standardized[field] = dataframe[source_column]

        # Use provided revenue, or calculate it from quantity and price.
        revenue_column = self.column_mapping["revenue"]
        unit_price_column = self.column_mapping["unit_price"]

        if revenue_column is not None:
            standardized["revenue"] = dataframe[revenue_column]
            self.revenue_calculation = "Source revenue column"
        else:
            standardized["revenue"] = (
                pd.to_numeric(
                    dataframe[self.column_mapping["quantity"]],
                    errors="coerce"
                )
                * pd.to_numeric(
                    dataframe[unit_price_column],
                    errors="coerce"
                )
            )
            self.revenue_calculation = "Quantity × Unit Price"

        # Count missing values before removing invalid rows.
        missing_values = int(
            standardized[
                ["date", "product", "region", "quantity", "revenue"]
            ].isna().sum().sum()
        )

        total_source_records = len(standardized)

        # Convert fields to appropriate data types.
        standardized["date"] = pd.to_datetime(
            standardized["date"],
            errors="coerce"
        )

        standardized["quantity"] = pd.to_numeric(
            standardized["quantity"],
            errors="coerce"
        )

        standardized["revenue"] = pd.to_numeric(
            standardized["revenue"],
            errors="coerce"
        )

        # Remove records with missing required values.
        before_cleanup = len(standardized)

        standardized = standardized.dropna(
            subset=[
                "date",
                "product",
                "region",
                "quantity",
                "revenue",
            ]
        )

        # Remove blank product and region names.
        standardized["product"] = (
            standardized["product"].astype(str).str.strip()
        )

        standardized["region"] = (
            standardized["region"].astype(str).str.strip()
        )

        standardized = standardized[
            (standardized["product"] != "")
            & (standardized["region"] != "")
        ]

        # Remove records with non-finite numeric values.
        numeric_valid = (
            standardized["quantity"].map(
                lambda value: pd.notna(value) and abs(value) != float("inf")
            )
            & standardized["revenue"].map(
                lambda value: pd.notna(value) and abs(value) != float("inf")
            )
        )

        standardized = standardized[numeric_valid]

        invalid_rows_removed = before_cleanup - len(standardized)

        # Count duplicate records in the original standardized data.
        duplicate_rows = int(standardized.duplicated().sum())

        # Keep valid records, including legitimate returns or adjustments.
        self.df = standardized.reset_index(drop=True)

        if self.df.empty:
            raise ValueError(
                "No valid sales records remain after data cleaning. "
                "Check the CSV columns and values."
            )

        self.quality_report = {
            "total_records": int(total_source_records),
            "valid_records": int(len(self.df)),
            "missing_values": missing_values,
            "invalid_rows_removed": int(invalid_rows_removed),
            "duplicate_rows": duplicate_rows,
        }

        return self.df

    def _ensure_data_loaded(self):
        if self.df is None:
            self.load_data()

    def get_overview(self):
        """Return high-level sales metrics."""

        self._ensure_data_loaded()

        total_revenue = float(self.df["revenue"].sum())
        total_quantity = float(self.df["quantity"].sum())
        total_transactions = int(len(self.df))

        average_transaction_value = (
            total_revenue / total_transactions
            if total_transactions > 0
            else 0
        )

        return {
            "total_revenue": total_revenue,
            "total_quantity": total_quantity,
            "total_transactions": total_transactions,
            "average_transaction_value": average_transaction_value,
        }

    def revenue_by_product(self):
        """Calculate revenue grouped by product."""

        self._ensure_data_loaded()

        return (
            self.df.groupby("product")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )

    def revenue_by_region(self):
        """Calculate revenue grouped by region."""

        self._ensure_data_loaded()

        return (
            self.df.groupby("region")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )

    def monthly_revenue(self):
        """Calculate revenue grouped by calendar month."""

        self._ensure_data_loaded()

        monthly = self.df.copy()

        monthly["month"] = monthly["date"].dt.to_period("M")

        return (
            monthly.groupby("month")["revenue"]
            .sum()
            .sort_index()
        )

    def get_data_quality(self):
        """Return data-quality metrics."""

        self._ensure_data_loaded()

        return self.quality_report.copy()
