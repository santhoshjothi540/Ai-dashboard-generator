import pandas as pd


def ask_ai(df, question):
    """
    Simple AI Chat for Dataset
    """

    question = question.lower().strip()

    # --------------------------------------------------
    # Total Records
    # --------------------------------------------------
    if "record" in question or "row" in question:
        return f"The dataset contains {len(df):,} records."

    # --------------------------------------------------
    # Total Columns
    # --------------------------------------------------
    elif "column" in question:
        return f"The dataset contains {len(df.columns)} columns."

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------
    elif "missing" in question:
        missing = int(df.isnull().sum().sum())
        return f"The dataset contains {missing:,} missing values."

    # --------------------------------------------------
    # Duplicate Rows
    # --------------------------------------------------
    elif "duplicate" in question:
        duplicates = int(df.duplicated().sum())
        return f"The dataset contains {duplicates:,} duplicate rows."

    # --------------------------------------------------
    # Fraud Count
    # --------------------------------------------------
    elif "fraud" in question:

        fraud_column = None

        for col in df.columns:
            if "fraud" in col.lower():
                fraud_column = col
                break

        if fraud_column:

            fraud_count = int(df[fraud_column].sum())

            return (
                f"The dataset contains "
                f"{fraud_count:,} fraudulent transactions."
            )

        return "No fraud column was found in the dataset."

    # --------------------------------------------------
    # Average Value
    # --------------------------------------------------
    elif "average" in question or "mean" in question:

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            return "No numerical columns found."

        column = numeric_cols[0]

        value = df[column].mean()

        return (
            f"The average value of '{column}' "
            f"is {value:.2f}."
        )

    # --------------------------------------------------
    # Maximum Value
    # --------------------------------------------------
    elif "maximum" in question or "highest" in question or "max" in question:

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            return "No numerical columns found."

        column = numeric_cols[0]

        value = df[column].max()

        return (
            f"The highest value in '{column}' "
            f"is {value:.2f}."
        )

    # --------------------------------------------------
    # Minimum Value
    # --------------------------------------------------
    elif "minimum" in question or "lowest" in question or "min" in question:

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            return "No numerical columns found."

        column = numeric_cols[0]

        value = df[column].min()

        return (
            f"The lowest value in '{column}' "
            f"is {value:.2f}."
        )

    # --------------------------------------------------
    # Dataset Information
    # --------------------------------------------------
    elif "dataset" in question or "summary" in question:

        return (
            f"The dataset has {len(df):,} rows and "
            f"{len(df.columns)} columns."
        )

    # --------------------------------------------------
    # Help
    # --------------------------------------------------
    elif "help" in question:

        return (
            "You can ask questions like:\n"
            "- How many records?\n"
            "- How many columns?\n"
            "- Missing values\n"
            "- Duplicate rows\n"
            "- Fraud count\n"
            "- Average value\n"
            "- Maximum value\n"
            "- Minimum value"
        )

    # --------------------------------------------------
    # Default Response
    # --------------------------------------------------
    else:
        return (
            "Sorry, I couldn't understand your question.\n\n"
            "Try asking:\n"
            "• How many records?\n"
            "• How many columns?\n"
            "• Missing values\n"
            "• Duplicate rows\n"
            "• Fraud count\n"
            "• Average value\n"
            "• Maximum value\n"
            "• Minimum value"
        )