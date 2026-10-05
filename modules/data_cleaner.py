import pandas as pd


def get_data_quality(df):
    """Check the quality of the uploaded dataset."""

    total_rows = len(df)
    total_columns = len(df.columns)
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    # --------------------------------------------------------------------
    # Per-column missing value breakdown (only columns that actually
    # have missing values are included)
    # --------------------------------------------------------------------
    missing_by_column = {
        column: int(count)
        for column, count in df.isnull().sum().items()
        if count > 0
    }

    total_cells = total_rows * total_columns if total_columns else 0
    missing_percentage = (
        round((missing_values / total_cells) * 100, 2)
        if total_cells > 0 else 0.0
    )
    duplicate_percentage = (
        round((duplicate_rows / total_rows) * 100, 2)
        if total_rows > 0 else 0.0
    )

    # --------------------------------------------------------------------
    # Simple, transparent quality score derived from missing/duplicate %.
    # 100 = perfect, reduced by how much data is missing or duplicated.
    # --------------------------------------------------------------------
    quality_score = round(
        max(0.0, 100 - missing_percentage - duplicate_percentage), 2
    )

    if quality_score >= 90:
        status = "Excellent"
    elif quality_score >= 75:
        status = "Good"
    elif quality_score >= 50:
        status = "Needs Attention"
    else:
        status = "Poor"

    numerical_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    other_columns = [
        column for column in df.columns
        if column not in numerical_columns and column not in categorical_columns
    ]

    quality = {
        # Original keys — unchanged, kept for backward compatibility
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "total_rows": total_rows,
        "total_columns": total_columns,

        # Aliases matching the keys app.py actually looks up
        "rows": total_rows,
        "columns": total_columns,

        # Richer information
        "missing_values_by_column": missing_by_column,
        "missing_percentage": missing_percentage,
        "duplicate_percentage": duplicate_percentage,
        "quality_score": quality_score,
        "status": status,
        "column_type_breakdown": {
            "numerical": len(numerical_columns),
            "categorical": len(categorical_columns),
            "other": len(other_columns),
        },
    }

    return quality


def clean_data(df):
    """Perform basic automatic data cleaning."""

    rows_before = len(df)

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    rows_after_dedup = len(cleaned_df)
    duplicates_removed = rows_before - rows_after_dedup

    # Fill missing numerical values with median
    numerical_columns = cleaned_df.select_dtypes(
        include="number"
    ).columns

    numeric_columns_filled = []

    for column in numerical_columns:
        if cleaned_df[column].isnull().any():
            missing_count = int(cleaned_df[column].isnull().sum())
            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].median()
            )
            numeric_columns_filled.append(
                {"column": column, "missing_filled": missing_count, "strategy": "median"}
            )

    # Fill missing categorical values with mode
    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category"]
    ).columns

    categorical_columns_filled = []

    for column in categorical_columns:
        if cleaned_df[column].isnull().any():
            mode_value = cleaned_df[column].mode()

            if not mode_value.empty:
                missing_count = int(cleaned_df[column].isnull().sum())
                cleaned_df[column] = cleaned_df[column].fillna(
                    mode_value[0]
                )
                categorical_columns_filled.append(
                    {"column": column, "missing_filled": missing_count, "strategy": "mode"}
                )

    # ----------------------------------------------------------------------
    # Attach a cleaning report as DataFrame metadata (pandas .attrs).
    # This does NOT change the return type — cleaned_df is still a plain
    # DataFrame, so existing calls like cleaned_df.head(10) keep working
    # exactly as before.
    # ----------------------------------------------------------------------
    cleaned_df.attrs["cleaning_report"] = {
        "rows_before": rows_before,
        "rows_after": len(cleaned_df),
        "duplicates_removed": duplicates_removed,
        "numeric_columns_filled": numeric_columns_filled,
        "categorical_columns_filled": categorical_columns_filled,
    }

    return cleaned_df
