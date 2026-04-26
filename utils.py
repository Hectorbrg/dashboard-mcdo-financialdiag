"""
Shared styling and helpers for the McDonald's dashboard.
Strict palette: Black / McDonald's European Green / McDonald's Yellow.
"""
import base64
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go


# ============================================================
# LOGO LOADER — looks for assets/mcdonalds_logo.png next to app.py
# Returns a base64 data URI for inline embedding, or None if missing.
# ============================================================
@st.cache_resource
def load_logo_data_uri():
    here = Path(__file__).resolve().parent
    candidates = [
        here / "assets" / "mcdonalds_logo.png",
        here / "assets" / "mcdonalds_logo.jpg",
        here / "mcdonalds_logo.png",
    ]
    for p in candidates:
        if p.exists():
            mime = "image/jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "image/png"
            return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"
    return None


# ============================================================
# DESIGN SYSTEM — strict palette
# ============================================================
BLACK       = "#000000"
GREEN       = "#008C42"   # McDonald's European Green
YELLOW      = "#FFC72C"   # McDonald's Yellow
WHITE       = "#FFFFFF"
OFF_WHITE   = "#F2F2F2"

# Neutral greys (the only non-brand colours we allow)
DARK_GREY   = "#141414"   # surfaces on black bg
MID_GREY    = "#2A2A2A"   # borders / dividers
SOFT_GREY   = "#3A3A3A"   # secondary surfaces / muted bars
SUBTLE      = "#9A9A9A"   # secondary text

# Cautionary tone — desaturated yellow (no red allowed by the brand)
DIM_YELLOW  = "#7A5E1A"

PLOTLY_FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"


# ============================================================
# NUMBER FORMATTERS — defensive, always return a printable string
# ============================================================
def fmt_money_m(value):
    """Input is in $M. Returns '$26.9B' for 26885 or '$774M' for 774."""
    if value is None:
        return "—"
    abs_v = abs(value)
    sign = "−" if value < 0 else ""
    if abs_v >= 1000:
        return f"{sign}${abs_v/1000:,.1f}B"
    return f"{sign}${abs_v:,.0f}M"


def fmt_pct(value, decimals=1):
    if value is None:
        return "—"
    return f"{value*100:,.{decimals}f}%"


def fmt_x(value, decimals=2):
    if value is None:
        return "—"
    return f"{value:,.{decimals}f}×"


def fmt_days(value, decimals=1):
    if value is None:
        return "—"
    return f"{value:,.{decimals}f}d"


def fmt_dollar(value, decimals=2):
    """Plain dollar amount (not in $M)."""
    if value is None:
        return "—"
    sign = "−" if value < 0 else ""
    return f"{sign}${abs(value):,.{decimals}f}"


def fmt_delta(curr, prev, mode="pct", inverse=False):
    """Return (delta_text, direction) where direction in {'up','down','neutral'}."""
    if curr is None or prev is None:
        return "—", "neutral"
    diff = curr - prev
    if diff == 0:
        return "0.0%" if mode == "pct" else "0.00", "neutral"
    if mode == "pct":
        if prev == 0:
            return "—", "neutral"
        text = f"{diff/abs(prev):+.1%}"
    else:
        text = f"{diff:+,.2f}"
    is_good = (diff < 0) if inverse else (diff > 0)
    return text, ("up" if is_good else "down")


# ============================================================
# CSS INJECTION
# ============================================================
GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: {PLOTLY_FONT} !important;
}}
.stApp {{ background: {BLACK}; color: {OFF_WHITE}; }}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {DARK_GREY};
    border-right: 1px solid {MID_GREY};
}}
section[data-testid="stSidebar"] * {{ color: {OFF_WHITE}; }}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1280px; }}

/* Headings */
h1, h2, h3, h4 {{
    font-family: {PLOTLY_FONT};
    color: {WHITE};
    letter-spacing: -0.01em;
}}
h1 {{ font-weight: 800; font-size: 2.1rem; letter-spacing: -0.02em; margin-bottom: 0.4rem; }}
h2 {{ font-weight: 700; font-size: 1.35rem; margin-top: 2.2rem; margin-bottom: 0.6rem; color: {WHITE}; }}
h3 {{
    font-weight: 600; font-size: 0.78rem; color: {YELLOW};
    text-transform: uppercase; letter-spacing: 0.16em;
    margin-top: 1.4rem; margin-bottom: 0.4rem;
}}
p, li, label {{ color: {OFF_WHITE}; line-height: 1.55; }}

/* Brand bar at the top */
.brand-bar {{
    display: flex; align-items: center; gap: 14px;
    padding: 14px 22px;
    background: {DARK_GREY};
    border-bottom: 1px solid {YELLOW};
    margin: -2.5rem -2.5rem 1.6rem -2.5rem;
}}
.brand-bar .logo-mark {{
    display: inline-block;
    width: 30px; height: 30px;
    background: {YELLOW};
    color: {BLACK};
    text-align: center; line-height: 30px;
    font-weight: 800; font-size: 17px;
    border-radius: 2px;
}}
.brand-bar .brand-title {{
    font-size: 12px; font-weight: 500;
    color: {SUBTLE};
    text-transform: uppercase; letter-spacing: 0.18em;
}}

/* KPI card */
.kpi {{
    background: {DARK_GREY};
    border: 1px solid {MID_GREY};
    border-top: 2px solid {YELLOW};
    border-radius: 3px;
    padding: 16px 18px 14px 18px;
    height: 130px;
    display: flex; flex-direction: column; justify-content: space-between;
    transition: border-top-color 0.2s ease;
}}
.kpi:hover {{ border-top-color: {GREEN}; }}
.kpi .label {{
    font-size: 10px; font-weight: 600;
    color: {SUBTLE};
    text-transform: uppercase; letter-spacing: 0.14em;
}}
.kpi .helper {{
    font-size: 11px; color: {SUBTLE}; margin-top: 2px;
}}
.kpi .value {{
    font-size: 1.75rem; font-weight: 700; color: {WHITE};
    line-height: 1.1; letter-spacing: -0.02em;
}}
.kpi .delta {{
    font-size: 0.78rem; font-weight: 600;
    display: inline-flex; align-items: center; gap: 4px;
}}
.kpi .delta.up      {{ color: {GREEN}; }}
.kpi .delta.down    {{ color: {DIM_YELLOW}; }}
.kpi .delta.neutral {{ color: {SUBTLE}; }}

/* Callout / one-line insight */
.callout {{
    background: {DARK_GREY};
    border-left: 2px solid {GREEN};
    padding: 10px 14px;
    margin: 4px 0 18px 0;
    font-size: 0.88rem; color: {OFF_WHITE};
    line-height: 1.5;
}}
.callout.warn {{ border-left-color: {YELLOW}; }}
.callout strong {{ color: {YELLOW}; font-weight: 600; }}

/* Compact gauge label */
.gauge-label {{
    color: {SUBTLE}; font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin-bottom: 0;
}}
.gauge-delta {{
    font-size: 0.78rem; font-weight: 500;
    margin-top: -8px; margin-bottom: 14px;
}}

/* Section divider */
.divider {{ height: 1px; background: {MID_GREY}; margin: 1.6rem 0; }}

/* Multiselect tags use brand green */
.stMultiSelect [data-baseweb="tag"] {{
    background: {GREEN} !important; color: {WHITE} !important;
}}

/* Radio in sidebar */
section[data-testid="stSidebar"] [role="radiogroup"] label {{
    padding: 6px 6px;
    border-radius: 2px;
}}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background: {MID_GREY};
}}

/* SWOT card */
.swot {{
    background: {DARK_GREY};
    border: 1px solid {MID_GREY};
    border-top: 2px solid {YELLOW};
    border-radius: 3px;
    padding: 18px 20px;
    height: 100%;
}}
.swot.ok    {{ border-top-color: {GREEN}; }}
.swot.warn  {{ border-top-color: {DIM_YELLOW}; }}
.swot h4 {{
    color: {YELLOW};
    margin: 0 0 12px 0;
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
}}
.swot.ok h4   {{ color: {GREEN}; }}
.swot.warn h4 {{ color: {YELLOW}; }}
.swot ul {{ list-style: none; padding: 0; margin: 0; }}
.swot li {{
    padding: 6px 0;
    border-bottom: 1px solid {MID_GREY};
    color: {OFF_WHITE}; font-size: 0.86rem; line-height: 1.45;
}}
.swot li:last-child {{ border-bottom: none; }}
.swot li b {{ color: {WHITE}; font-weight: 600; }}
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_brand_bar():
    logo_uri = load_logo_data_uri()
    if logo_uri:
        logo_html = (
            f'<img src="{logo_uri}" alt="McDonald\'s" '
            f'style="height:36px;width:auto;display:block;" />'
        )
    else:
        logo_html = '<span class="logo-mark">M</span>'
    st.markdown(
        f"""
        <div class="brand-bar">
            {logo_html}
            <span class="brand-title">McDonald's Corporation &middot; Financial Diagnosis &middot; FY 2023–2025</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_divider():
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


# ============================================================
# KPI CARD
# ============================================================
def kpi_card(label, value, delta_text=None, delta_dir="neutral", helper=None):
    arrow = {"up": "▲", "down": "▼", "neutral": "•"}.get(delta_dir, "•")
    delta_html = ""
    if delta_text and delta_text != "—":
        delta_html = (
            f"<div class='delta {delta_dir}'>{arrow}&nbsp;{delta_text}"
            f"<span style='color:{SUBTLE};font-weight:400;'>&nbsp;YoY</span></div>"
        )
    elif delta_text == "—":
        delta_html = f"<div class='delta neutral'>—</div>"

    helper_html = f"<div class='helper'>{helper}</div>" if helper else ""
    st.markdown(
        f"""
        <div class="kpi">
            <div>
                <div class="label">{label}</div>
                {helper_html}
            </div>
            <div>
                <div class="value">{value}</div>
                {delta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(text, kind="default"):
    """Single-line insight under a chart. kind in {'default','warn'}."""
    cls = "callout" + (" warn" if kind == "warn" else "")
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


# ============================================================
# PLOTLY BASE LAYOUT
# ============================================================
def base_layout(height=360, show_legend=True):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=PLOTLY_FONT, color=OFF_WHITE, size=12),
        margin=dict(l=10, r=10, t=22, b=30),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=OFF_WHITE, size=11),
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            color=SUBTLE, linecolor=MID_GREY,
            tickfont=dict(color=OFF_WHITE),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=MID_GREY, gridwidth=0.5, zeroline=False,
            color=SUBTLE, tickfont=dict(color=OFF_WHITE),
        ),
        hoverlabel=dict(
            bgcolor=DARK_GREY, bordercolor=YELLOW,
            font=dict(color=WHITE, family=PLOTLY_FONT),
        ),
    )


# ============================================================
# CHART HELPERS
# ============================================================
def _safe(values):
    """Replace None with 0 for plotting; return mask of valid points too."""
    return [0 if v is None else v for v in values]


def line_chart(years, series_dict, y_format="$,.0f", height=320):
    """series_dict: {label: [values]} — colours cycle YELLOW → GREEN → WHITE."""
    palette = [YELLOW, GREEN, WHITE]

    if y_format == "$B":
        scale = 1000.0
        axis_tickformat = "$,.1f"
        axis_ticksuffix = "B"
        hover_fmt = "$%{y:.2f}B"
    else:
        scale = 1.0
        axis_tickformat = y_format
        axis_ticksuffix = ""
        hover_fmt = "%{y:" + y_format + "}"

    fig = go.Figure()
    for i, (label, values) in enumerate(series_dict.items()):
        c = palette[i % len(palette)]
        # Drop None pairs so the line doesn't crash; scale the remaining points
        clean_x = [x for x, v in zip(years, values) if v is not None]
        clean_y = [v / scale for v in values if v is not None]
        if not clean_y:
            continue
        fig.add_trace(go.Scatter(
            x=clean_x, y=clean_y, mode="lines+markers",
            name=label,
            line=dict(color=c, width=3),
            marker=dict(size=10, color=c, line=dict(color=BLACK, width=2)),
            hovertemplate="<b>%{x}</b><br>" + label + ": " + hover_fmt + "<extra></extra>",
        ))
    layout = base_layout(height=height)
    layout["xaxis"]["tickmode"] = "array"
    layout["xaxis"]["tickvals"] = years
    layout["yaxis"]["tickformat"] = axis_tickformat
    if axis_ticksuffix:
        layout["yaxis"]["ticksuffix"] = axis_ticksuffix
    fig.update_layout(**layout)
    return fig


def bar_chart(years, series_dict, y_format="$,.0f", height=320, mode="group"):
    palette = [YELLOW, GREEN, SOFT_GREY]

    # "$B" is a special mode: input values are in $M, axis displays in billions.
    if y_format == "$B":
        scale = 1000.0
        axis_tickformat = "$,.1f"
        axis_ticksuffix = "B"
        hover_fmt = "$%{y:.2f}B"
    else:
        scale = 1.0
        axis_tickformat = y_format
        axis_ticksuffix = ""
        hover_fmt = "%{y:" + y_format + "}"

    fig = go.Figure()
    for i, (label, values) in enumerate(series_dict.items()):
        c = palette[i % len(palette)]
        scaled = [(0 if v is None else v) / scale for v in values]
        fig.add_trace(go.Bar(
            x=years, y=scaled, name=label,
            marker_color=c, marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>" + label + ": " + hover_fmt + "<extra></extra>",
        ))
    layout = base_layout(height=height)
    layout["barmode"] = mode
    layout["bargap"] = 0.40
    layout["xaxis"]["tickmode"] = "array"
    layout["xaxis"]["tickvals"] = years
    layout["yaxis"]["tickformat"] = axis_tickformat
    if axis_ticksuffix:
        layout["yaxis"]["ticksuffix"] = axis_ticksuffix
    fig.update_layout(**layout)
    return fig


def donut_chart(labels, values, height=300, colors=None):
    if colors is None:
        colors = [GREEN, YELLOW, SOFT_GREY, MID_GREY]
    # Convert from $M to $B for both display and hover
    values_b = [(v / 1000.0) if v is not None else 0 for v in values]
    total_b = sum(values_b)
    fig = go.Figure(go.Pie(
        labels=labels, values=values_b, hole=0.65,
        marker=dict(colors=colors, line=dict(color=BLACK, width=2)),
        textinfo="label+percent",
        textfont=dict(color=WHITE, size=11, family=PLOTLY_FONT),
        hovertemplate="<b>%{label}</b><br>$%{value:.2f}B (%{percent})<extra></extra>",
        sort=False,
    ))
    layout = base_layout(height=height, show_legend=False)
    layout["margin"] = dict(l=10, r=10, t=10, b=10)
    fig.update_layout(**layout)
    fig.add_annotation(
        text=f"<b>${total_b:,.1f}B</b><br><span style='font-size:10px;color:{SUBTLE}'>TOTAL</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=WHITE, size=18, family=PLOTLY_FONT),
    )
    return fig


def bullet_gauge(value, zones, ideal_range, value_format="number",
                 higher_is_better=True, height=100):
    """Horizontal gauge with three benchmark zones (dim → mid → bright)
    and a marker for the actual value."""
    z0, z1, z2, z3 = zones
    # Zone tints — only green/yellow/dim-yellow allowed
    if higher_is_better:
        zone_colors = [
            "rgba(122,94,26,0.45)",   # weak (dim yellow)
            "rgba(255,199,44,0.40)",  # mid (yellow)
            "rgba(0,140,66,0.50)",    # strong (green)
        ]
    else:
        zone_colors = [
            "rgba(0,140,66,0.50)",    # strong (green) — low values are good
            "rgba(255,199,44,0.40)",  # mid
            "rgba(122,94,26,0.45)",   # weak
        ]

    if value_format == "percent":
        display_val = "—" if value is None else f"{value*100:.1f}%"
    elif value_format == "x":
        display_val = "—" if value is None else f"{value:.2f}×"
    elif value_format == "days":
        display_val = "—" if value is None else f"{value:.1f}d"
    else:
        display_val = "—" if value is None else f"{value:,.2f}"

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[z1 - z0], y=[0], orientation="h", base=z0,
                         marker=dict(color=zone_colors[0]),
                         hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Bar(x=[z2 - z1], y=[0], orientation="h", base=z1,
                         marker=dict(color=zone_colors[1]),
                         hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Bar(x=[z3 - z2], y=[0], orientation="h", base=z2,
                         marker=dict(color=zone_colors[2]),
                         hoverinfo="skip", showlegend=False))
    # Ideal-range outline (dotted green box)
    fig.add_shape(
        type="rect",
        x0=ideal_range[0], x1=ideal_range[1], y0=-0.18, y1=0.18,
        line=dict(color=GREEN, width=1.5, dash="dot"),
        fillcolor="rgba(0,0,0,0)",
    )
    # Value marker (yellow vertical tick)
    if value is not None:
        clamped = max(z0, min(value, z3))
        fig.add_trace(go.Scatter(
            x=[clamped], y=[0], mode="markers",
            marker=dict(symbol="line-ns", size=46, color=YELLOW,
                        line=dict(color=BLACK, width=3)),
            hovertemplate=f"Value: {display_val}<extra></extra>",
            showlegend=False,
        ))
        # Number annotation above the tick
        fig.add_annotation(
            x=clamped, y=0.45, text=f"<b>{display_val}</b>",
            showarrow=False, font=dict(color=YELLOW, size=14, family=PLOTLY_FONT),
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=PLOTLY_FONT, color=OFF_WHITE, size=11),
        height=height,
        margin=dict(l=4, r=4, t=10, b=22),
        barmode="overlay",
        bargap=0.3,
        showlegend=False,
        xaxis=dict(range=[z0, z3], showgrid=False, zeroline=False,
                   color=SUBTLE, tickfont=dict(color=OFF_WHITE, size=10)),
        yaxis=dict(visible=False, range=[-0.55, 0.6]),
    )
    return fig


def heatmap_matrix(years, ratio_dict, height=460):
    """Heatmap of ratios x years.
    Colour intensity reflects how a ratio has changed vs the first year shown.
    Cells display the actual ratio value."""
    rows, normalised = [], []
    for label, vals in ratio_dict.items():
        rows.append(label)
        first = next((v for v in vals if v is not None), None)
        if first is None or first == 0:
            normalised.append([0 if v is not None else None for v in vals])
        else:
            normalised.append([
                ((v / first) - 1) if v is not None else None
                for v in vals
            ])

    text = []
    for label, vals in ratio_dict.items():
        row_text = []
        for v in vals:
            if v is None:
                row_text.append("—")
            elif "%" in label or "margin" in label.lower() or "ROCE" in label or "ROA" in label or "payout" in label.lower() or "yield" in label.lower():
                row_text.append(f"{v*100:.1f}%")
            elif "ratio" in label.lower() or "turnover" in label.lower() or "coverage" in label.lower() or "EBITDA" in label or "P/E" in label:
                row_text.append(f"{v:.2f}×")
            elif "day" in label.lower() or "CCC" in label:
                row_text.append(f"{v:.1f}d")
            else:
                row_text.append(f"{v:,.2f}")
        text.append(row_text)

    fig = go.Figure(go.Heatmap(
        z=normalised, x=[str(y) for y in years], y=rows,
        text=text, texttemplate="%{text}",
        textfont=dict(color=WHITE, size=11, family=PLOTLY_FONT),
        colorscale=[[0, "#3a2e0e"], [0.5, MID_GREY], [1, GREEN]],
        zmid=0,
        showscale=False,
        hovertemplate="<b>%{y}</b><br>%{x}: %{text}<extra></extra>",
        xgap=2, ygap=2,
    ))
    layout = base_layout(height=height, show_legend=False)
    layout["margin"] = dict(l=10, r=10, t=10, b=20)
    layout["yaxis"] = dict(autorange="reversed", color=OFF_WHITE,
                           tickfont=dict(color=OFF_WHITE, size=11), automargin=True)
    layout["xaxis"] = dict(
        side="top", color=YELLOW,
        tickfont=dict(color=YELLOW, size=12, family=PLOTLY_FONT),
        type="category",
        tickmode="array",
        tickvals=[str(y) for y in years],
        ticktext=[str(y) for y in years],
    )
    fig.update_layout(**layout)
    return fig
