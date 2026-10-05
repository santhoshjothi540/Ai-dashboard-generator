import io
import os
import json
import re
from xml.sax.saxutils import escape

import numpy as np
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def detect_time_column(df):
    dates = df.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    if dates:
        return dates[0]

    for c in df.columns:
        if any(
            k in str(c).lower()
            for k in ("date", "datetime", "timestamp")
        ):
            p = pd.to_datetime(df[c], errors="coerce")

            if p.notna().mean() >= 0.7:
                return c

    return None


def relationship_report(df):
    nums = df.select_dtypes(include="number")

    if nums.shape[1] < 2:
        return pd.DataFrame(
            columns=[
                "Column A",
                "Column B",
                "Correlation",
                "Strength"
            ]
        )

    corr = nums.corr()
    rows = []
    cols = list(corr.columns)

    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            v = corr.loc[a, b]

            if pd.isna(v):
                continue

            av = abs(float(v))

            strength = (
                "Strong"
                if av >= 0.7
                else "Moderate"
                if av >= 0.4
                else "Weak"
            )

            rows.append(
                {
                    "Column A": a,
                    "Column B": b,
                    "Correlation": round(float(v), 3),
                    "Strength": strength
                }
            )

    if rows:
        return pd.DataFrame(rows).sort_values(
            "Correlation",
            key=lambda s: s.abs(),
            ascending=False
        )

    return pd.DataFrame(
        columns=[
            "Column A",
            "Column B",
            "Correlation",
            "Strength"
        ]
    )


def forecast(df):
    t = detect_time_column(df)

    nums = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if not t:
        return None, "No date/time column detected."

    if not nums:
        return None, "No numeric metric available for forecasting."

    metric = next(
        (
            c
            for c in nums
            if any(
                k in str(c).lower()
                for k in (
                    "revenue",
                    "sales",
                    "profit",
                    "amount",
                    "value",
                    "score"
                )
            )
        ),
        nums[0]
    )

    x = df[[t, metric]].copy()

    x[t] = pd.to_datetime(
        x[t],
        errors="coerce"
    )

    x[metric] = pd.to_numeric(
        x[metric],
        errors="coerce"
    )

    x = x.dropna().sort_values(t)

    if len(x) < 8:
        return (
            None,
            "At least 8 time observations are recommended for forecasting."
        )

    g = x.groupby(
        t,
        as_index=False
    )[metric].sum()

    g["step"] = np.arange(len(g))

    horizon = min(
        12,
        max(4, len(g) // 4)
    )

    coef = np.polyfit(
        g["step"],
        g[metric],
        1
    )

    future_step = np.arange(
        len(g),
        len(g) + horizon
    )

    pred = np.polyval(
        coef,
        future_step
    )

    delta = (
        g[t]
        .diff()
        .dropna()
        .median()
    )

    delta = (
        delta
        if pd.notna(delta)
        and delta > pd.Timedelta(0)
        else pd.Timedelta(days=1)
    )

    future_dates = pd.date_range(
        g[t].max() + delta,
        periods=horizon,
        freq=delta
    )

    return {
        "history": g[[t, metric]],
        "forecast": pd.DataFrame(
            {
                t: future_dates,
                metric: pred
            }
        ),
        "metric": metric
    }, None


def data_drilldown(df, dimension, value):
    if dimension not in df.columns:
        return df

    return df[
        df[dimension].astype(str) == str(value)
    ].copy()


def clean_insight_for_pdf(text):
    """
    Converts HTML/CSS based insight text into
    safe plain text for ReportLab.

    This prevents ReportLab Paragraph from failing
    on unsupported HTML attributes such as:
    class, display, background, border-radius, etc.
    """

    text = str(text)

    # Convert common HTML line-break tags to new lines
    text = re.sub(
        r"<\s*br\s*/?\s*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Add spacing for block-level elements
    text = re.sub(
        r"</\s*(div|p|section|article|h[1-6])\s*>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Remove all remaining HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # Convert common HTML entities safely
    text = (
        text
        .replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )

    # Remove excessive blank spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Clean excessive newlines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


def make_report_pdf(df, insights, profile):
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    story = [
        Paragraph(
            "AI Dashboard Report",
            styles["Title"]
        ),
        Spacer(1, 12),

        Paragraph(
            f"Rows: {len(df):,} | "
            f"Columns: {len(df.columns)} | "
            f"Missing values: {int(df.isna().sum().sum()):,}",
            styles["BodyText"]
        ),

        Spacer(1, 12),

        Paragraph(
            "Automated Insights",
            styles["Heading2"]
        )
    ]

    # ---------------------------------------------------------
    # FIX:
    # Clean HTML/CSS insights before passing them to ReportLab
    # ---------------------------------------------------------

    if insights is None:
        insights = []

    # Handle a single string insight
    if isinstance(insights, str):
        insights = [insights]

    for x in insights:

        clean_text = clean_insight_for_pdf(x)

        if not clean_text:
            continue

        # Escape special XML characters so ReportLab
        # doesn't interpret user/data text as HTML.
        clean_text = escape(clean_text)

        story += [
            Paragraph(
                clean_text,
                styles["BodyText"]
            ),
            Spacer(1, 5)
        ]

    # ---------------------------------------------------------
    # Sample Data
    # ---------------------------------------------------------

    sample = df.head(12).astype(str)

    data = [
        list(sample.columns[:8])
    ] + sample.iloc[:, :8].values.tolist()

    table = Table(
        data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#222222")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story += [
        Spacer(1, 12),

        Paragraph(
            "Sample Data",
            styles["Heading2"]
        ),

        table
    ]

    doc.build(story)

    buf.seek(0)

    return buf