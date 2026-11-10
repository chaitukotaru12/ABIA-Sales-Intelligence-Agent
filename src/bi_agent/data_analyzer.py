
from pathlib import Path

import pandas as pd


class DatasetAnalyzer:
    """
    Universal CSV analyzer for structured business datasets.

    Supports sales, revenue, profit, expenses, finance,
    transactions, inventory and other business data.

    Preserves original columns and dynamically identifies
    numeric, categorical, datetime and identifier columns.

    Legacy sales methods remain available when the required
    sales columns exist.
    """

    DATE_ALIASES = {
        "date", "order date", "transaction date", "invoice date",
        "purchase date", "created at", "updated at", "timestamp",
        "payment date", "booking date", "sales date"
    }

    ID_ALIASES = {
        "id", "order id", "transaction id", "invoice id",
        "customer id", "account id", "record id", "reference",
        "reference number", "serial number"
    }

    SEMANTIC_ALIASES = {
        "date": [
            "date", "order date", "transaction date", "invoice date",
            "purchase date", "sales date"
        ],
        "product": [
            "product", "product name", "productname",
            "item", "item name", "description"
        ],
        "region": [
            "region", "country", "market", "territory",
            "state", "sales region"
        ],
        "quantity": [
            "quantity", "qty", "units", "units sold",
            "unit sold", "order quantity"
        ],
        "revenue": [
            "revenue", "sales", "amount", "total sales",
            "total revenue", "sales amount", "line total",
            "total amount"
        ],
        "unit_price": [
            "unit price", "unitprice", "price per unit",
            "price", "unit cost"
        ]
    }

    def __init__(self, data_path):
        self.data_path = Path(data_path)

        self.raw_df = None
        self.df = None
        self.column_metadata = {}
        self.quality_report = {}
        self.profile = {}
        self.encoding_used = None
        self.semantic_columns = {}

    @staticmethod
    def _normalize_column_name(column):
        return (
            str(column)
            .strip()
            .lower()
            .replace("_", " ")
            .replace("-", " ")
            .replace(".", " ")
        ).strip()

    def _read_csv(self):
        """Read CSV using common text encodings."""

        encodings = ["utf-8-sig", "utf-8", "cp1252", "latin1"]
        last_error = None

        for encoding in encodings:
            try:
                dataframe = pd.read_csv(
                    self.data_path,
                    encoding=encoding
                )
                self.encoding_used = encoding
                return dataframe

            except UnicodeDecodeError as error:
                last_error = error

        raise ValueError(
            f"Unable to decode CSV file: {last_error}"
        )

    def _find_semantic_column(self, dataframe, aliases):
        """Find a source column matching a known semantic alias."""

        normalized_aliases = {
            self._normalize_column_name(alias)
            for alias in aliases
        }

        for column in dataframe.columns:
            normalized = self._normalize_column_name(column)

            if normalized in normalized_aliases:
                return column

        return None

    def _detect_semantic_columns(self, dataframe):
        """Discover common business fields without requiring them."""

        return {
            field: self._find_semantic_column(dataframe, aliases)
            for field, aliases in self.SEMANTIC_ALIASES.items()
        }

    def _detect_column_metadata(self, dataframe):
        """Discover the likely role and type of every column."""

        metadata = {}

        for column in dataframe.columns:
            series = dataframe[column]
            normalized = self._normalize_column_name(column)

            non_null = series.dropna()
            unique_count = int(series.nunique(dropna=True))

            is_identifier = (
                normalized in self.ID_ALIASES
                or normalized.endswith(" id")
                or normalized.endswith(" number")
            )

            # Explicitly named date columns are recognized directly.
            is_date = normalized in self.DATE_ALIASES

            # Only attempt automatic date detection on non-numeric data.
            if (
                not is_date
                and not is_identifier
                and not pd.api.types.is_numeric_dtype(series)
                and not non_null.empty
            ):
                parsed_dates = pd.to_datetime(
                    non_null,
                    errors="coerce",
                    format="mixed"
                )

                date_ratio = parsed_dates.notna().mean()

                is_date = (
                    date_ratio >= 0.85
                    and non_null.nunique() > 1
                )

            numeric_values = pd.to_numeric(
                series,
                errors="coerce"
            )

            numeric_ratio = (
                numeric_values.notna().mean()
                if len(series) > 0 else 0
            )

            if is_identifier:
                column_type = "identifier"

            elif is_date:
                column_type = "datetime"

            elif numeric_ratio >= 0.85 and series.notna().any():
                column_type = "numeric"

            else:
                column_type = "categorical"

            metadata[str(column)] = {
                "type": column_type,
                "missing_values": int(series.isna().sum()),
                "unique_values": unique_count,
                "non_null_values": int(series.notna().sum())
            }

        return metadata

    def _clean_dataframe(self, dataframe):
        """Clean recognized data types without imposing sales rules."""

        cleaned = dataframe.copy()

        for column in cleaned.columns:
            column_type = self.column_metadata[str(column)]["type"]

            if column_type == "datetime":
                cleaned[column] = pd.to_datetime(
                    cleaned[column],
                    errors="coerce",
                    format="mixed"
                )

            elif column_type == "numeric":
                cleaned[column] = pd.to_numeric(
                    cleaned[column],
                    errors="coerce"
                )

            elif column_type == "categorical":
                if (
                    pd.api.types.is_object_dtype(cleaned[column])
                    or isinstance(cleaned[column].dtype, pd.StringDtype)
                ):
                    cleaned[column] = cleaned[column].map(
                        lambda value: (
                            value.strip()
                            if isinstance(value, str)
                            else value
                        )
                    )

        return cleaned

    def load_data(self):
        """Load, profile and clean a business CSV."""

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.data_path}"
            )

        dataframe = self._read_csv()

        if dataframe.empty:
            raise ValueError("The uploaded CSV file is empty.")

        if len(dataframe.columns) == 0:
            raise ValueError("The CSV file contains no columns.")

        if dataframe.columns.duplicated().any():
            raise ValueError(
                "The CSV contains duplicate column names. "
                "Please make the column names unique."
            )

        self.raw_df = dataframe.copy()

        original_records = len(dataframe)
        missing_values = int(dataframe.isna().sum().sum())
        duplicate_rows = int(dataframe.duplicated().sum())

        self.column_metadata = self._detect_column_metadata(
            dataframe
        )

        self.semantic_columns = self._detect_semantic_columns(
            dataframe
        )

        cleaned = self._clean_dataframe(dataframe)

        # Remove only completely empty records.
        before_cleanup = len(cleaned)
        cleaned = cleaned.dropna(how="all")
        empty_rows_removed = before_cleanup - len(cleaned)

        invalid_numeric_values = 0

        for column in cleaned.columns:
            if self.column_metadata[str(column)]["type"] == "numeric":
                original_non_null = dataframe.loc[
                    cleaned.index, column
                ].notna()

                converted_null = cleaned[column].isna()

                invalid_numeric_values += int(
                    (original_non_null & converted_null).sum()
                )

        self.df = cleaned.reset_index(drop=True)

        if self.df.empty:
            raise ValueError(
                "No usable records remain after data cleaning."
            )

        numeric_columns = [
            column
            for column, details in self.column_metadata.items()
            if details["type"] == "numeric"
        ]

        categorical_columns = [
            column
            for column, details in self.column_metadata.items()
            if details["type"] == "categorical"
        ]

        datetime_columns = [
            column
            for column, details in self.column_metadata.items()
            if details["type"] == "datetime"
        ]

        identifier_columns = [
            column
            for column, details in self.column_metadata.items()
            if details["type"] == "identifier"
        ]

        self.quality_report = {
            "total_records": int(original_records),
            "valid_records": int(len(self.df)),
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "empty_rows_removed": int(empty_rows_removed),
            "invalid_rows_removed": int(empty_rows_removed),
            "invalid_numeric_values": int(invalid_numeric_values),
            "encoding": self.encoding_used
        }

        self.profile = {
            "row_count": int(len(self.df)),
            "column_count": int(len(self.df.columns)),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "datetime_columns": datetime_columns,
            "identifier_columns": identifier_columns,
            "columns": self.column_metadata
        }

        return self.df

    def _ensure_data_loaded(self):
        if self.df is None:
            self.load_data()

    def _require_semantic_columns(self, *fields):
        """Ensure a legacy sales operation has the required columns."""

        self._ensure_data_loaded()

        missing = [
            field
            for field in fields
            if self.semantic_columns.get(field) is None
        ]

        if missing:
            raise ValueError(
                "This analysis requires these dataset fields: "
                + ", ".join(missing)
            )

    def get_profile(self):
        """Return the discovered dataset schema."""

        self._ensure_data_loaded()
        return self.profile.copy()

    def get_column_metadata(self):
        """Return metadata for every detected column."""

        self._ensure_data_loaded()
        return self.column_metadata.copy()

    def get_data_quality(self):
        """Return dataset quality metrics."""

        self._ensure_data_loaded()
        return self.quality_report.copy()

    def get_overview(self):
        """Return generic statistics and available legacy sales KPIs."""

        self._ensure_data_loaded()

        numeric_summary = {}

        for column in self.profile["numeric_columns"]:
            series = self.df[column].dropna()

            numeric_summary[column] = {
                "sum": float(series.sum()),
                "mean": float(series.mean()) if not series.empty else None,
                "minimum": float(series.min()) if not series.empty else None,
                "maximum": float(series.max()) if not series.empty else None
            }

        date_ranges = {}

        for column in self.profile["datetime_columns"]:
            series = self.df[column].dropna()

            if not series.empty:
                date_ranges[column] = {
                    "minimum": str(series.min()),
                    "maximum": str(series.max())
                }

        overview = {
            "total_records": int(len(self.df)),
            "total_columns": int(len(self.df.columns)),
            "numeric_columns": self.profile["numeric_columns"],
            "categorical_columns": self.profile["categorical_columns"],
            "datetime_columns": self.profile["datetime_columns"],
            "identifier_columns": self.profile["identifier_columns"],
            "numeric_summary": numeric_summary,
            "date_ranges": date_ranges
        }

        # Legacy sales KPIs are included only when available.
        revenue_column = self.semantic_columns.get("revenue")
        quantity_column = self.semantic_columns.get("quantity")

        if revenue_column is not None:
            revenue = pd.to_numeric(
                self.df[revenue_column],
                errors="coerce"
            ).dropna()

            overview["total_revenue"] = float(revenue.sum())

            overview["average_transaction_value"] = (
                float(revenue.sum() / len(self.df))
                if len(self.df) > 0 else 0.0
            )

        if quantity_column is not None:
            quantity = pd.to_numeric(
                self.df[quantity_column],
                errors="coerce"
            )

            overview["total_quantity"] = float(quantity.sum())

        if revenue_column is not None or quantity_column is not None:
            overview["total_transactions"] = int(len(self.df))

        return overview

    def revenue_by_product(self):
        """Legacy method: calculate revenue grouped by product."""

        self._require_semantic_columns("product", "revenue")

        product_column = self.semantic_columns["product"]
        revenue_column = self.semantic_columns["revenue"]

        return (
            self.df.groupby(product_column)[revenue_column]
            .sum()
            .sort_values(ascending=False)
        )

    def revenue_by_region(self):
        """Legacy method: calculate revenue grouped by region."""

        self._require_semantic_columns("region", "revenue")

        region_column = self.semantic_columns["region"]
        revenue_column = self.semantic_columns["revenue"]

        return (
            self.df.groupby(region_column)[revenue_column]
            .sum()
            .sort_values(ascending=False)
        )

    def monthly_revenue(self):
        """Legacy method: calculate revenue grouped by month."""

        self._require_semantic_columns("date", "revenue")

        date_column = self.semantic_columns["date"]
        revenue_column = self.semantic_columns["revenue"]

        monthly = self.df[[date_column, revenue_column]].copy()
        monthly["month"] = monthly[date_column].dt.to_period("M")

        return (
            monthly.groupby("month")[revenue_column]
            .sum()
            .sort_index()
        )


# Temporary compatibility alias for existing imports.
SalesAnalyzer = DatasetAnalyzer
