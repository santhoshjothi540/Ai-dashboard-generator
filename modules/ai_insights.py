import pandas as pd


# ==============================================================================
# STYLE HELPERS (premium SaaS-style insight badges)
# ==============================================================================
_BADGE_STYLE_INJECTED = False

_GRADIENTS = {
    "overview": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)",
    "positive": "linear-gradient(135deg, #22C55E 0%, #16A34A 100%)",
    "warning": "linear-gradient(135deg, #F59E0B 0%, #F43F5E 100%)",
    "numeric": "linear-gradient(135deg, #6366F1 0%, #06B6D4 100%)",
    "categorical": "linear-gradient(135deg, #06B6D4 0%, #6366F1 100%)",
    "correlation": "linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)",
}


def _inject_badge_style_once() -> str:
    """Return a one-time <style> block for badge hover micro-animation.

    This is only emitted with the first insight of each call so the
    hover/transition rules exist in the DOM without repeating them on
    every single card.
    """
    global _BADGE_STYLE_INJECTED
    if _BADGE_STYLE_INJECTED:
        return ""
    _BADGE_STYLE_INJECTED = True
    return """
        <style>
            .ai-insight-badge {
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }
            .ai-insight-badge:hover {
                transform: translateY(-1px) scale(1.04);
                box-shadow: 0 6px 16px rgba(99, 102, 241, 0.35);
            }
        </style>
    """


def _format_insight(icon: str, category: str, text: str, gradient_key: str) -> str:
    """Wrap a plain-text insight into a premium glass/gradient badge + typography block."""
    gradient = _GRADIENTS.get(gradient_key, _GRADIENTS["overview"])
    style_block = _inject_badge_style_once()

    return (
        f"{style_block}"
        f'<span class="ai-insight-badge" style="'
        f"display:inline-flex;align-items:center;gap:6px;"
        f"padding:4px 12px;border-radius:999px;"
        f"background:{gradient};"
        f"backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);"
        f"box-shadow:0 4px 12px rgba(0,0,0,0.25);"
        f"font-size:0.7rem;font-weight:700;letter-spacing:0.5px;"
        f'text-transform:uppercase;color:#ffffff;margin-bottom:8px;">'
        f"{icon} {category}"
        f"</span>"
        f'<div style="font-size:0.95rem;line-height:1.6;color:#F5F5F7;'
        f'font-weight:400;letter-spacing:-0.1px;">{text}</div>'
    )


# ==============================================================================
# AI INSIGHTS GENERATION (backend logic — unchanged)
# ==============================================================================
def generate_insights(df):

    insights = []

    # Basic dataset information
    rows = len(df)
    columns = len(df.columns)

    insights.append(
        _format_insight(
            "🗂️", "Dataset Overview",
            f"The dataset contains <b>{rows:,}</b> records across "
            f"<b>{columns}</b> columns.",
            "overview",
        )
    )

    # Missing values
    missing_values = int(df.isnull().sum().sum())

    if missing_values == 0:
        insights.append(
            _format_insight(
                "✅", "Data Completeness",
                "No missing values were detected in the dataset.",
                "positive",
            )
        )
    else:
        insights.append(
            _format_insight(
                "⚠️", "Missing Data",
                f"The dataset contains <b>{missing_values:,}</b> missing "
                f"values that may require attention.",
                "warning",
            )
        )

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    if duplicate_rows == 0:
        insights.append(
            _format_insight(
                "✅", "Data Integrity",
                "No duplicate records were detected.",
                "positive",
            )
        )
    else:
        insights.append(
            _format_insight(
                "🔁", "Duplicate Records",
                f"<b>{duplicate_rows:,}</b> duplicate records were detected.",
                "warning",
            )
        )

    # Numerical analysis
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numerical_columns:

        for column in numerical_columns[:5]:

            mean_value = df[column].mean()
            max_value = df[column].max()
            min_value = df[column].min()

            if pd.notna(mean_value):

                insights.append(
                    _format_insight(
                        "📈", f"{column}",
                        f"Average value of <b>{mean_value:.2f}</b>, with "
                        f"values ranging from <b>{min_value:.2f}</b> to "
                        f"<b>{max_value:.2f}</b>.",
                        "numeric",
                    )
                )

    # Categorical analysis
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical_columns:

        for column in categorical_columns[:3]:

            unique_count = df[column].nunique()

            insights.append(
                _format_insight(
                    "🏷️", f"{column}",
                    f"Contains <b>{unique_count:,}</b> unique categories.",
                    "categorical",
                )
            )

    # Correlation analysis
    if len(numerical_columns) >= 2:

        correlation = df[numerical_columns].corr()

        max_pair = None
        max_corr = 0

        for i in range(len(correlation.columns)):

            for j in range(i + 1, len(correlation.columns)):

                value = correlation.iloc[i, j]

                if pd.notna(value) and abs(value) > abs(max_corr):

                    max_corr = value

                    max_pair = (
                        correlation.columns[i],
                        correlation.columns[j]
                    )

        if max_pair:

            insights.append(
                _format_insight(
                    "🔗", "Strongest Relationship",
                    f"<b>{max_pair[0]}</b> and <b>{max_pair[1]}</b> show the "
                    f"strongest relationship, with a correlation of "
                    f"<b>{max_corr:.2f}</b>.",
                    "correlation",
                )
            )

    return insights
