import pandas as pd


# ==============================================================================
# STYLE / CLASSIFICATION HELPERS (derived from the same IQR bounds —
# no change to which rows are detected as outliers)
# ==============================================================================
def _classify_anomaly(value, lower, upper, iqr):
    """Classify a single outlier value into score / severity / risk level / color / reason.

    The classification is entirely derived from how far the value sits
    beyond the already-computed IQR bounds — it does not alter which
    values are flagged as outliers.
    """

    if value < lower:
        deviation = lower - value
        direction = "below the lower IQR bound"
    else:
        deviation = value - upper
        direction = "above the upper IQR bound"

    if iqr and iqr > 0:
        normalized = deviation / iqr
    else:
        normalized = deviation if deviation > 0 else 0.0

    # Squash the (unbounded) normalized deviation into a 0-1 score,
    # where values further outside the IQR bounds score closer to 1.
    score = round(min(0.99, normalized / (normalized + 1)), 3)

    if score >= 0.75:
        severity, risk_level, color = "Critical", "High Risk", "#F43F5E"
    elif score >= 0.50:
        severity, risk_level, color = "High", "Elevated Risk", "#F97316"
    elif score >= 0.25:
        severity, risk_level, color = "Medium", "Moderate Risk", "#F59E0B"
    else:
        severity, risk_level, color = "Low", "Low Risk", "#FACC15"

    reason = (
        f"Value is {direction} "
        f"(deviation of {deviation:.2f}, {normalized:.2f}x the IQR)."
    )

    return score, severity, risk_level, color, reason


# ==============================================================================
# ANOMALY DETECTION (IQR logic — unchanged)
# ==============================================================================
def detect_anomalies(df):

    results = {}

    numerical_columns = df.select_dtypes(include="number").columns

    for column in numerical_columns:

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[column] < lower) |
            (df[column] > upper)
        ].copy()

        # --------------------------------------------------------------
        # Enrich each detected outlier row with Severity, Risk Level,
        # Reason, Score, and Color — computed from the same lower/upper
        # bounds used for detection above.
        # --------------------------------------------------------------
        if not outliers.empty:

            scores = []
            severities = []
            risk_levels = []
            colors = []
            reasons = []

            for value in outliers[column]:

                score, severity, risk_level, color, reason = _classify_anomaly(
                    value, lower, upper, iqr
                )

                scores.append(score)
                severities.append(severity)
                risk_levels.append(risk_level)
                colors.append(color)
                reasons.append(reason)

            outliers["anomaly_score"] = scores
            outliers["severity"] = severities
            outliers["risk_level"] = risk_levels
            outliers["color"] = colors
            outliers["reason"] = reasons

        results[column] = outliers

    return results
