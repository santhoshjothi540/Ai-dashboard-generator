import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

PREMIUM_COLORWAY = ["#6366F1", "#8B5CF6", "#3B82F6", "#06B6D4", "#22C55E", "#F59E0B", "#F43F5E"]
_FONT_FAMILY = "Inter, Segoe UI, Arial, sans-serif"


def _apply_premium_theme(fig, height=450, show_legend=False):
    fig.update_layout(template="plotly_dark", height=height, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family=_FONT_FAMILY, color="#F5F5F7"),
                      margin=dict(l=45,r=30,t=70,b=45), showlegend=show_legend,
                      legend=dict(orientation="h", y=1.08))
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
    return fig


def _detect_time_column(df):
    dates = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
    if dates: return dates[0]
    for c in df.columns:
        if any(k in str(c).lower() for k in ("date", "datetime", "timestamp")):
            p = pd.to_datetime(df[c], errors="coerce")
            if p.notna().mean() >= .7: return c
    return None


def _is_id_like(s):
    return s.nunique(dropna=True) >= max(20, int(len(s)*.95))


def _numeric_metric(df):
    nums=df.select_dtypes(include="number").columns.tolist()
    keywords=("revenue","sales","amount","profit","income","price","cost","value","score","cgpa")
    for c in nums:
        if any(k in str(c).lower() for k in keywords): return c
    return nums[0] if nums else None


def _categorical_dimension(df):
    cats=df.select_dtypes(include=["object","category","bool"]).columns.tolist()
    for c in cats:
        if 1 < df[c].nunique() <= min(50, max(2, len(df)//2)) and not _is_id_like(df[c]): return c
    return None


def _time_chart(df, time_col, metric):
    x=df[[time_col,metric]].copy(); x[time_col]=pd.to_datetime(x[time_col],errors="coerce"); x[metric]=pd.to_numeric(x[metric],errors="coerce"); x=x.dropna()
    if x.empty: return None
    try: g=x.set_index(time_col)[metric].resample("ME").sum().reset_index()
    except Exception: g=x.groupby(time_col,as_index=False)[metric].sum()
    fig=px.line(g,x=time_col,y=metric,markers=True,title=f"{metric} Trend",color_discrete_sequence=PREMIUM_COLORWAY)
    return _apply_premium_theme(fig,420,False)


def smart_chart(df, metric=None, dimension=None, time_col=None, aggregation="sum", chart_type="auto"):
    nums=df.select_dtypes(include="number").columns.tolist(); cats=df.select_dtypes(include=["object","category","bool"]).columns.tolist()
    if metric not in nums: metric=_numeric_metric(df)
    if dimension not in cats: dimension=_categorical_dimension(df)
    if time_col not in df.columns: time_col=_detect_time_column(df)
    if chart_type in (None,"auto"):
        chart_type="line" if time_col and metric else "bar" if dimension and metric else "histogram" if metric else "pie" if dimension else "none"
    if chart_type=="line" and time_col and metric: return _time_chart(df,time_col,metric)
    if chart_type in ("bar","grouped_bar") and dimension and metric:
        g=df.groupby(dimension,dropna=False)[metric].mean() if aggregation in ("mean","average") else df.groupby(dimension,dropna=False)[metric].sum()
        g=g.reset_index().sort_values(metric,ascending=False).head(15)
        fig=px.bar(g,x=dimension,y=metric,title=f"{metric} by {dimension}",color=dimension,color_discrete_sequence=PREMIUM_COLORWAY,text_auto=".2s")
        return _apply_premium_theme(fig,450,False)
    if chart_type=="pie" and dimension:
        g=df[dimension].value_counts().head(10).reset_index(); g.columns=[dimension,"Count"]
        fig=px.pie(g,names=dimension,values="Count",title=f"Distribution of {dimension}",hole=.45,color_discrete_sequence=PREMIUM_COLORWAY)
        fig.update_traces(textinfo="percent+label",marker=dict(line=dict(color="#0C0D12",width=2)))
        return _apply_premium_theme(fig,450,True)
    if chart_type in ("scatter","scatter_plot") and len(nums)>=2:
        x=metric or nums[0]; y=next((n for n in nums if n!=x),nums[1])
        fig=px.scatter(df,x=x,y=y,title=f"{x} vs {y}",opacity=.65,color_discrete_sequence=PREMIUM_COLORWAY)
        return _apply_premium_theme(fig,450,False)
    if chart_type in ("histogram","distribution") and metric:
        fig=px.histogram(df,x=metric,marginal="box",title=f"Distribution of {metric}",color_discrete_sequence=PREMIUM_COLORWAY)
        fig.update_traces(marker_line_color="rgba(255,255,255,.12)",marker_line_width=1,opacity=.9)
        return _apply_premium_theme(fig,450,False)
    return None


def generate_charts(df):
    """Automatic domain-independent dashboard charts; preserves original palette."""
    charts=[]; nums=df.select_dtypes(include="number").columns.tolist(); cats=df.select_dtypes(include=["object","category","bool"]).columns.tolist(); time=_detect_time_column(df); metric=_numeric_metric(df); dim=_categorical_dimension(df)
    if time and metric:
        f=smart_chart(df,metric=metric,time_col=time,chart_type="line")
        if f is not None: charts.append(("Trend",f))
    if dim and metric:
        f=smart_chart(df,metric=metric,dimension=dim,chart_type="bar")
        if f is not None: charts.append(("Category Breakdown",f))
    if metric:
        f=smart_chart(df,metric=metric,chart_type="histogram")
        if f is not None: charts.append(("Distribution",f))
    if dim:
        f=smart_chart(df,dimension=dim,chart_type="pie")
        if f is not None: charts.append(("Category Mix",f))
    if len(nums)>=2:
        f=smart_chart(df,metric=nums[0],chart_type="scatter")
        if f is not None: charts.append(("Relationship",f))
        corr=df[nums].corr()
        f=px.imshow(corr,text_auto=True,title="Correlation Heatmap",aspect="auto",color_continuous_scale=[[0,"#3B82F6"],[.5,"#0C0D12"],[1,"#A855F7"]],range_color=[-1,1])
        f=_apply_premium_theme(f,500,False); charts.append(("Correlation Heatmap",f))
    return charts
