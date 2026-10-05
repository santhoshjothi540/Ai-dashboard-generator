import pandas as pd


def get_data_profile(df):
    """Generate basic information about the uploaded dataset."""

    rows = len(df)
    columns = len(df.columns)
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns
    boolean_cols = df.select_dtypes(include="bool").columns

    total_cells = rows * columns if columns else 0
    completeness_percentage = (
        round(100 - (missing_values / total_cells) * 100, 2)
        if total_cells > 0 else 0.0
    )
    duplicate_percentage = (
        round((duplicate_rows / rows) * 100, 2)
        if rows > 0 else 0.0
    )

    # --------------------------------------------------------------------
    # Numeric summary (min / mean / max) — useful for premium KPI-style
    # dashboard widgets, purely derived from existing numeric columns.
    # --------------------------------------------------------------------
    numeric_summary = {}
    for column in numeric_cols:
        series = df[column]
        numeric_summary[column] = {
            "min": float(series.min()) if pd.notna(series.min()) else None,
            "mean": float(series.mean()) if pd.notna(series.mean()) else None,
            "max": float(series.max()) if pd.notna(series.max()) else None,
        }

    # --------------------------------------------------------------------
    # Categorical summary (top value + how many unique categories)
    # --------------------------------------------------------------------
    categorical_summary = {}
    for column in categorical_cols:
        mode_series = df[column].mode()
        categorical_summary[column] = {
            "unique_values": int(df[column].nunique()),
            "top_value": str(mode_series.iloc[0]) if not mode_series.empty else None,
        }

    memory_usage_mb = round(
        df.memory_usage(deep=True).sum() / (1024 * 1024), 3
    )

    profile = {
        # Original keys — unchanged, kept for backward compatibility
        "rows": rows,
        "columns": columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numeric_columns": len(numeric_cols),
        "categorical_columns": len(categorical_cols),

        # Richer statistics for a premium dashboard
        "datetime_columns": len(datetime_cols),
        "boolean_columns": len(boolean_cols),
        "completeness_percentage": completeness_percentage,
        "duplicate_percentage": duplicate_percentage,
        "memory_usage_mb": memory_usage_mb,
        "column_names": df.columns.tolist(),
        "numeric_summary": numeric_summary,
        "categorical_summary": categorical_summary,
    }

    return profile


def get_column_info(df):
    """Return information about each column."""

    rows = len(df)

    missing_counts = df.isnull().sum()
    unique_counts = df.nunique()

    missing_percentages = []
    sample_values = []
    most_frequent_values = []
    quality_flags = []

    for column in df.columns:

        missing_count = int(missing_counts[column])
        unique_count = int(unique_counts[column])

        missing_pct = round((missing_count / rows) * 100, 2) if rows > 0 else 0.0
        missing_percentages.append(missing_pct)

        non_null_series = df[column].dropna()
        sample_values.append(
            str(non_null_series.iloc[0]) if not non_null_series.empty else "N/A"
        )

        mode_series = df[column].mode()
        most_frequent_values.append(
            str(mode_series.iloc[0]) if not mode_series.empty else "N/A"
        )

        if missing_pct > 50:
            flag = "High Missing"
        elif unique_count == 1:
            flag = "Constant"
        elif unique_count == rows and rows > 0:
            flag = "Likely Unique/ID"
        else:
            flag = "OK"
        quality_flags.append(flag)

    column_info = pd.DataFrame({
        # Original columns — unchanged, kept for backward compatibility
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values,

        # Richer columns for a premium dashboard
        "Missing %": missing_percentages,
        "Sample Value": sample_values,
        "Most Frequent": most_frequent_values,
        "Quality Flag": quality_flags,
    })

    return column_info
