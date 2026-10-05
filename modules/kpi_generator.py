import pandas as pd

# Preserve the original project's visual palette.
_COLOR_INDIGO = "#6366F1"
_COLOR_BLUE = "#3B82F6"
_COLOR_VIOLET = "#8B5CF6"
_COLOR_GREEN = "#22C55E"
_COLOR_AMBER = "#F59E0B"
_COLOR_RED = "#F43F5E"
_COLOR_GRAY = "#6B6B76"


def _detect_time_column(df):
    dates = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    if dates:
        return dates[0]
    for c in df.columns:
        if any(k in str(c).lower() for k in ("date", "datetime", "timestamp")):
            parsed = pd.to_datetime(df[c], errors="coerce")
            if parsed.notna().mean() >= 0.7:
                return c
    return None


def _fmt(v):
    if pd.isna(v): return "—"
    if abs(v) >= 1_000_000: return f"{v/1_000_000:.2f}M"
    if abs(v) >= 1_000: return f"{v/1_000:.2f}K"
    return f"{v:,.2f}"


def _trend(df, time_col, metric):
    if not time_col or metric not in df.columns or len(df) < 4:
        return None
    x = df[[time_col, metric]].copy()
    x["_t"] = pd.to_datetime(x[time_col], errors="coerce")
    x[metric] = pd.to_numeric(x[metric], errors="coerce")
    x = x.dropna().sort_values("_t")
    if len(x) < 4 or x["_t"].nunique() < 2: return None
    cut = x["_t"].min() + (x["_t"].max() - x["_t"].min()) / 2
    a, b = x[x["_t"] <= cut][metric], x[x["_t"] > cut][metric]
    if a.empty or b.empty: return None
    av, bv = a.mean(), b.mean()
    if av == 0: return None
    delta = (bv-av)/abs(av)*100
    return {"direction": "up" if delta > 0 else "down" if delta < 0 else "flat", "delta": round(delta,1), "label": f"{abs(delta):.1f}% vs previous period"}


def _card(key, title, value, icon, color, trend=None):
    return {"key": key, "title": title, "value": value, "icon": icon, "color": color,
            "status": "neutral", "trend": trend or {"direction": None, "delta": None, "label": "Dataset metric"}}


def _candidate_metric(df):
    nums = df.select_dtypes(include="number").columns.tolist()
    if not nums: return None
    # Prefer meaningful business metrics but never assume one exists.
    keywords = ("revenue", "sales", "amount", "profit", "income", "price", "cost", "value", "score", "cgpa")
    for c in nums:
        if any(k in str(c).lower() for k in keywords): return c
    return nums[0]


def generate_kpis(df):
    """Generate domain-independent KPIs. No fraud/transaction assumptions."""
    n = len(df)
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    time_col = _detect_time_column(df)
    metric = _candidate_metric(df)

    cards = [_card("total_records", "Total Records", f"{n:,}", "📄", _COLOR_INDIGO)]
    cards.append(_card("columns", "Columns", f"{len(df.columns):,}", "🧱", _COLOR_BLUE))

    if metric:
        s = pd.to_numeric(df[metric], errors="coerce").dropna()
        if not s.empty:
            cards.append(_card("primary_metric", f"Avg {metric}", _fmt(s.mean()), "📊", _COLOR_VIOLET, _trend(df,time_col,metric)))
            cards.append(_card("primary_total", f"Total {metric}", _fmt(s.sum()), "Σ", _COLOR_GREEN, _trend(df,time_col,metric)))

    if categorical:
        c = categorical[0]
        cards.append(_card("categories", f"{c} Groups", f"{df[c].nunique():,}", "🏷️", _COLOR_BLUE))
    elif numeric:
        cards.append(_card("numeric_metrics", "Numeric Metrics", f"{len(numeric):,}", "🔢", _COLOR_BLUE))

    if time_col:
        cards.append(_card("time_range", "Time Coverage", f"{df[time_col].nunique():,} points", "🕒", _COLOR_INDIGO))
    else:
        cards.append(_card("missing", "Missing Values", f"{int(df.isna().sum().sum()):,}", "⚠️", _COLOR_AMBER))

    return {"cards": cards, "total_records": n, "metric_column": metric, "time_column": time_col,
            "numeric_columns": numeric, "categorical_columns": categorical}
