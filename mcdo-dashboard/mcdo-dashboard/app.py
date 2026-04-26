"""
McDonald's Corporation — Executive Financial Dashboard
======================================================
Concise, visual-first companion to the underlying Excel analysis.
FY 2023 / 2024 / 2025.

Run with:
    streamlit run app.py
"""
import streamlit as st
import plotly.graph_objects as go

from data.financials import (
    YEARS, INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW,
    RATIOS, RATIO_BENCHMARKS, SWOT,
)
from utils import (
    BLACK, GREEN, YELLOW, WHITE, OFF_WHITE,
    DARK_GREY, MID_GREY, SOFT_GREY, SUBTLE, DIM_YELLOW,
    PLOTLY_FONT,
    fmt_money_m, fmt_pct, fmt_x, fmt_days, fmt_dollar, fmt_delta,
    inject_global_css, render_brand_bar, section_divider,
    kpi_card, callout,
    base_layout, line_chart, bar_chart, donut_chart,
    bullet_gauge, heatmap_matrix,
)


# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="McDonald's · Financial Diagnosis FY23–25",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()


# =====================================================================
# DATA HELPERS
# =====================================================================
@st.cache_data
def get_data():
    return {"is": INCOME_STATEMENT, "bs": BALANCE_SHEET,
            "cf": CASH_FLOW, "ratios": RATIOS}

D = get_data()


def row(book, key):
    return D[book][key]


def value(book, key, year):
    return D[book][key][YEARS.index(year)]


# =====================================================================
# SIDEBAR — navigation + filters (no emojis)
# =====================================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin:6px 0 10px 0;">
            <span style="display:inline-block;width:28px;height:28px;background:{YELLOW};
                         color:{BLACK};text-align:center;line-height:28px;font-weight:800;
                         font-size:15px;border-radius:2px;">M</span>
            <span style="font-size:10px;font-weight:600;color:{SUBTLE};
                         text-transform:uppercase;letter-spacing:0.16em;line-height:1.3;">
                Financial<br/>Diagnosis
            </span>
        </div>
        <div style="height:1px;background:{MID_GREY};margin:14px 0 18px 0;"></div>
        """,
        unsafe_allow_html=True,
    )

    PAGES = ["Overview", "Profitability", "Capital & Liquidity", "Verdict"]
    page = st.radio("NAVIGATION", PAGES, label_visibility="collapsed")

    st.markdown(
        f"<div style='height:1px;background:{MID_GREY};margin:18px 0;'></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='font-size:10px;font-weight:700;color:{YELLOW};"
        f"letter-spacing:0.18em;text-transform:uppercase;margin-bottom:10px;'>Filters</div>",
        unsafe_allow_html=True,
    )

    selected_years = st.multiselect(
        "Fiscal years",
        options=YEARS,
        default=YEARS,
        help="Filter the years shown in trend charts.",
    )
    if not selected_years:
        selected_years = YEARS

    view_mode = st.radio(
        "Display mode",
        ["Absolute", "YoY % change"],
        index=0,
        help="Toggle dollar amounts vs year-over-year change.",
    )

    st.markdown(
        f"<div style='height:1px;background:{MID_GREY};margin:22px 0 12px 0;'></div>"
        f"<div style='font-size:10px;color:{SUBTLE};line-height:1.55;'>"
        "Source: McDonald's 10-K filings, FY 2023–2025. All figures in USD millions "
        "unless stated. The dashboard is a visual companion to the workbook."
        "</div>",
        unsafe_allow_html=True,
    )

# Working filter state
FY = [y for y in YEARS if y in selected_years]


def filter_series(values):
    """Return (years_filtered, values_filtered) honouring the year filter
    and the absolute-vs-YoY toggle."""
    if view_mode == "YoY % change":
        full = [None] + [
            None if (values[i-1] in (0, None) or values[i] is None)
            else (values[i] - values[i-1]) / abs(values[i-1])
            for i in range(1, len(values))
        ]
        out_y, out_v = [], []
        for y in FY:
            i = YEARS.index(y)
            out_y.append(y)
            out_v.append(full[i])
        return out_y, out_v
    pairs = [(y, values[YEARS.index(y)]) for y in FY]
    return [p[0] for p in pairs], [p[1] for p in pairs]


# =====================================================================
# RENDER
# =====================================================================
render_brand_bar()


# ─────────────────────────────────────────────────────────────────────
# PAGE 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────
if page == "Overview":
    st.markdown(
        f"""
        <h1>A capital-return franchise<br/>
        <span style='color:{YELLOW};'>running on textbook discipline.</span></h1>
        <p style='color:{SUBTLE};font-size:1rem;max-width:680px;margin-top:0;'>
        Three years of consistent execution. Industry-leading margins, predictable cash flow,
        and the entire operating surplus returned to shareholders.</p>
        """,
        unsafe_allow_html=True,
    )

    section_divider()

    # ----- Hero KPIs -----
    rev = row("is", "Total revenues")
    ni  = row("is", "Net income")
    op  = row("ratios", "Operating margin (EBIT / Revenue)")
    fcf = row("cf",  "Free Cash Flow (CFO - CapEx)")
    eps = row("is", "EPS — basic ($)")
    div = row("is", "Dividends declared per share ($)")

    cols = st.columns(3, gap="medium")
    metrics_top = [
        ("Total Revenue",    fmt_money_m(rev[-1]), *fmt_delta(rev[-1], rev[-2]), "FY 2025"),
        ("Net Income",       fmt_money_m(ni[-1]),  *fmt_delta(ni[-1], ni[-2]),   "After tax"),
        ("Operating Margin", fmt_pct(op[-1]),       *fmt_delta(op[-1], op[-2], mode="abs"), "EBIT / Revenue"),
    ]
    for col, m in zip(cols, metrics_top):
        with col:
            kpi_card(*m)

    cols = st.columns(3, gap="medium")
    metrics_bot = [
        ("Free Cash Flow",   fmt_money_m(fcf[-1]),    *fmt_delta(fcf[-1], fcf[-2]), "CFO − CapEx"),
        ("EPS (basic)",      fmt_dollar(eps[-1]),     *fmt_delta(eps[-1], eps[-2]), "Per share"),
        ("Dividend / Share", fmt_dollar(div[-1]),     *fmt_delta(div[-1], div[-2]), "Declared"),
    ]
    for col, m in zip(cols, metrics_bot):
        with col:
            kpi_card(*m)

    section_divider()

    # ----- Two anchor charts -----
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("### Revenue & Operating Income")
        years_out, rev_out = filter_series(rev)
        _,         opi_out = filter_series(row("is", "Operating income (EBIT)"))
        if view_mode == "YoY % change":
            fig = line_chart(years_out, {"Revenue": rev_out, "Operating income": opi_out},
                             y_format=".1%", height=300)
        else:
            fig = bar_chart(years_out, {"Revenue": rev_out, "Operating income": opi_out},
                            y_format="$,.0f", height=300)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        callout(
            f"Operating income grew <strong>+5.8%</strong> against +3.7% revenue in FY25 "
            f"— positive operating leverage, the signature of a healthy franchise model."
        )

    with c2:
        st.markdown("### Three-margin trio")
        op_m  = row("ratios", "Operating margin (EBIT / Revenue)")
        ebd_m = row("ratios", "EBITDA margin")
        net_m = row("ratios", "Net margin (Net income / Revenue)")
        years_out, op_out  = filter_series(op_m)
        _, ebd_out = filter_series(ebd_m)
        _, net_out = filter_series(net_m)
        fig = line_chart(
            years_out,
            {"EBITDA margin": ebd_out, "Operating margin": op_out, "Net margin": net_out},
            y_format=".1%", height=300,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        callout(
            "All three margins expanded in FY25. <strong>46% operating margin</strong> "
            "and <strong>48% EBITDA margin</strong> — best-in-class for any consumer business."
        )

    section_divider()

    # ----- The negative-equity teaching moment (signature visual) -----
    st.markdown("### Why book equity is negative")
    c1, c2 = st.columns([1.4, 1], gap="large")

    with c1:
        retained = row("bs", "Retained earnings")
        treasury = row("bs", "Common stock in treasury, at cost")
        equity   = row("bs", "Total shareholders' equity (deficit)")
        years_out = [y for y in YEARS if y in FY]
        re_out = [retained[YEARS.index(y)] for y in years_out]
        tr_out = [treasury[YEARS.index(y)] for y in years_out]
        eq_out = [equity[YEARS.index(y)]   for y in years_out]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Retained earnings", x=years_out, y=re_out,
            marker_color=GREEN, marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Retained earnings: $%{y:,.0f}M<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            name="Treasury stock (buybacks)", x=years_out, y=tr_out,
            marker_color=DIM_YELLOW, marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Treasury stock: $%{y:,.0f}M<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            name="Total equity", x=years_out, y=eq_out,
            mode="lines+markers+text",
            line=dict(color=YELLOW, width=3, dash="dot"),
            marker=dict(size=11, color=YELLOW, line=dict(color=BLACK, width=2)),
            text=[fmt_money_m(v) for v in eq_out],
            textposition="top center",
            textfont=dict(color=YELLOW, size=11, family=PLOTLY_FONT),
            hovertemplate="<b>%{x}</b><br>Total equity: $%{y:,.0f}M<extra></extra>",
        ))
        layout = base_layout(height=380)
        layout["barmode"] = "relative"
        layout["xaxis"]["tickmode"] = "array"
        layout["xaxis"]["tickvals"] = years_out
        layout["yaxis"]["tickformat"] = "$,.0f"
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown(
            f"""
            <div style="padding:10px 0 0 0;">
                <div style="font-size:0.78rem;font-weight:700;color:{YELLOW};
                            letter-spacing:0.18em;text-transform:uppercase;margin-bottom:8px;">
                    The mechanic
                </div>
                <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:4px;">
                    <span style="font-size:2.2rem;font-weight:800;color:{GREEN};
                                letter-spacing:-0.02em;">$70B</span>
                    <span style="color:{SUBTLE};font-size:0.9rem;">retained earnings</span>
                </div>
                <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:14px;">
                    <span style="font-size:2.2rem;font-weight:800;color:{DIM_YELLOW};
                                letter-spacing:-0.02em;">−$79B</span>
                    <span style="color:{SUBTLE};font-size:0.9rem;">treasury stock</span>
                </div>
                <div style="height:1px;background:{MID_GREY};margin:8px 0 14px 0;"></div>
                <p style="color:{OFF_WHITE};font-size:0.92rem;line-height:1.55;margin:0;">
                Cumulative buybacks now exceed cumulative profits. Equity is negative by design,
                not by distress. <strong style='color:{YELLOW};'>ROE, D/E and P/B are
                mathematically meaningless</strong> — replaced here by ROCE, ROA, and Net Debt/EBITDA.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────
# PAGE 2 — PROFITABILITY
# ─────────────────────────────────────────────────────────────────────
elif page == "Profitability":
    st.markdown("<h1>Profitability & Returns</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{SUBTLE};font-size:0.95rem;max-width:660px;margin-top:-4px;'>"
        "How efficiently revenue becomes operating profit, cash, and shareholder return."
        "</p>",
        unsafe_allow_html=True,
    )

    section_divider()

    # ----- KPI strip -----
    cols = st.columns(4, gap="medium")
    metrics = [
        ("Operating margin", fmt_pct(row("ratios", "Operating margin (EBIT / Revenue)")[-1]),
         *fmt_delta(row("ratios", "Operating margin (EBIT / Revenue)")[-1],
                    row("ratios", "Operating margin (EBIT / Revenue)")[-2], mode="abs"),
         "EBIT / Revenue"),
        ("EBITDA margin", fmt_pct(row("ratios", "EBITDA margin")[-1]),
         *fmt_delta(row("ratios", "EBITDA margin")[-1],
                    row("ratios", "EBITDA margin")[-2], mode="abs"),
         "Pre-financing"),
        ("ROCE", fmt_pct(row("ratios", "ROCE (NOPAT / Capital Employed)")[-1]),
         *fmt_delta(row("ratios", "ROCE (NOPAT / Capital Employed)")[-1],
                    row("ratios", "ROCE (NOPAT / Capital Employed)")[-2], mode="abs"),
         "NOPAT / Capital empl."),
        ("ROA", fmt_pct(row("ratios", "ROA (Net income / Total assets)")[-1]),
         *fmt_delta(row("ratios", "ROA (Net income / Total assets)")[-1],
                    row("ratios", "ROA (Net income / Total assets)")[-2], mode="abs"),
         "Net income / Assets"),
    ]
    for col, m in zip(cols, metrics):
        with col:
            kpi_card(*m)

    section_divider()

    # ----- Margin gauges (3-up) -----
    st.markdown("### Margins vs benchmark zones")
    cols = st.columns(3, gap="large")
    margin_ratios = [
        "Operating margin (EBIT / Revenue)",
        "EBITDA margin",
        "Net margin (Net income / Revenue)",
    ]
    for col, ratio_name in zip(cols, margin_ratios):
        with col:
            v = row("ratios", ratio_name)[-1]
            v_prev = row("ratios", ratio_name)[-2]
            b = RATIO_BENCHMARKS[ratio_name]
            st.markdown(
                f"<div class='gauge-label'>{ratio_name.split(' (')[0]}</div>",
                unsafe_allow_html=True,
            )
            fig = bullet_gauge(
                v, b["zones"], b["ideal"],
                value_format="percent",
                higher_is_better=b["higher_is_better"],
                height=110,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            d_txt, d_dir = fmt_delta(v, v_prev, mode="abs")
            arrow = {"up":"▲","down":"▼","neutral":"•"}[d_dir]
            color = {"up":GREEN,"down":DIM_YELLOW,"neutral":SUBTLE}[d_dir]
            st.markdown(
                f"<div class='gauge-delta' style='color:{color};'>"
                f"{arrow}&nbsp;{d_txt} vs FY24</div>",
                unsafe_allow_html=True,
            )

    callout(
        "Three-margin lift in FY25. Yellow tick on each gauge sits inside the green ideal "
        "zone — McDonald's runs in the top decile of any restaurant or consumer business."
    )

    section_divider()

    # ----- ROCE / ROA gauges -----
    st.markdown("### Returns on capital")
    c1, c2 = st.columns(2, gap="large")
    for col, ratio_name in zip([c1, c2],
        ["ROCE (NOPAT / Capital Employed)", "ROA (Net income / Total assets)"]):
        with col:
            v = row("ratios", ratio_name)[-1]
            v_prev = row("ratios", ratio_name)[-2]
            b = RATIO_BENCHMARKS[ratio_name]
            st.markdown(
                f"<div class='gauge-label'>{ratio_name.split(' (')[0]}</div>",
                unsafe_allow_html=True,
            )
            fig = bullet_gauge(
                v, b["zones"], b["ideal"],
                value_format="percent",
                higher_is_better=True, height=110,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            d_txt, d_dir = fmt_delta(v, v_prev, mode="abs")
            arrow = {"up":"▲","down":"▼","neutral":"•"}[d_dir]
            color = {"up":GREEN,"down":DIM_YELLOW,"neutral":SUBTLE}[d_dir]
            st.markdown(
                f"<div class='gauge-delta' style='color:{color};'>"
                f"{arrow}&nbsp;{d_txt} vs FY24</div>",
                unsafe_allow_html=True,
            )

    callout(
        f"<strong>16% ROCE</strong> against ~7% cost of capital — every dollar deployed earns "
        "~9 percentage points of economic spread. ROE is intentionally omitted (negative equity)."
    )

    section_divider()

    # ----- Capital return machine -----
    st.markdown("### The capital-return machine")
    c1, c2 = st.columns([1.4, 1], gap="large")
    with c1:
        years_out = [y for y in YEARS if y in FY]
        divs = [-value("cf", "Common stock dividends", y) for y in years_out]
        bbk  = [-value("cf", "Treasury stock purchases", y) for y in years_out]
        fcf_v = [value("cf", "Free Cash Flow (CFO - CapEx)", y) for y in years_out]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Dividends", x=years_out, y=divs,
                             marker_color=GREEN, marker_line_width=0,
                             hovertemplate="<b>%{x}</b><br>Dividends: $%{y:,.0f}M<extra></extra>"))
        fig.add_trace(go.Bar(name="Buybacks", x=years_out, y=bbk,
                             marker_color=YELLOW, marker_line_width=0,
                             hovertemplate="<b>%{x}</b><br>Buybacks: $%{y:,.0f}M<extra></extra>"))
        fig.add_trace(go.Scatter(name="Free Cash Flow", x=years_out, y=fcf_v,
                                 mode="lines+markers+text",
                                 line=dict(color=WHITE, width=3, dash="dot"),
                                 marker=dict(size=10, color=WHITE,
                                            line=dict(color=BLACK, width=2)),
                                 text=[fmt_money_m(v) for v in fcf_v],
                                 textposition="top center",
                                 textfont=dict(color=WHITE, size=11, family=PLOTLY_FONT),
                                 hovertemplate="<b>%{x}</b><br>FCF: $%{y:,.0f}M<extra></extra>"))
        layout = base_layout(height=380)
        layout["barmode"] = "stack"
        layout["xaxis"]["tickmode"] = "array"
        layout["xaxis"]["tickvals"] = years_out
        layout["yaxis"]["tickformat"] = "$,.0f"
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        total_returned = (
            -row("cf", "Common stock dividends")[-1]
            -row("cf", "Treasury stock purchases")[-1]
        )
        cur_fcf = row("cf", "Free Cash Flow (CFO - CapEx)")[-1]
        coverage = total_returned / cur_fcf
        payout = row("ratios", "Dividend payout ratio")[-1]
        yield_ = row("ratios", "Dividend yield")[-1]
        st.markdown(
            f"""
            <div style='padding:10px 0;'>
                <div style='color:{SUBTLE};font-size:0.78rem;font-weight:600;
                            letter-spacing:0.16em;text-transform:uppercase;'>FY 2025</div>
                <div style='font-size:2.4rem;font-weight:800;color:{YELLOW};
                            line-height:1.1;letter-spacing:-0.02em;'>
                    {fmt_money_m(total_returned)}</div>
                <div style='color:{OFF_WHITE};font-size:0.92rem;margin-top:4px;'>
                    returned to shareholders<br/>
                    <span style='color:{SUBTLE};'>({coverage*100:.0f}% of FCF)</span>
                </div>
                <div style='height:1px;background:{MID_GREY};margin:18px 0;'></div>
                <div style='display:flex;justify-content:space-between;
                            color:{OFF_WHITE};font-size:0.88rem;margin-bottom:8px;'>
                    <span>Payout ratio</span>
                    <span style='color:{YELLOW};font-weight:600;'>{payout*100:.0f}%</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                            color:{OFF_WHITE};font-size:0.88rem;margin-bottom:8px;'>
                    <span>Dividend yield</span>
                    <span style='color:{YELLOW};font-weight:600;'>{yield_*100:.2f}%</span>
                </div>
                <div style='display:flex;justify-content:space-between;
                            color:{OFF_WHITE};font-size:0.88rem;'>
                    <span>Buyback yield</span>
                    <span style='color:{YELLOW};font-weight:600;'>~1.0%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    callout(
        "Capital returned absorbs the entire free cash flow every year — the very mechanism "
        "that drives book equity negative.",
        kind="warn",
    )

    section_divider()

    # ----- Revenue mix (franchised vs company-owned) -----
    st.markdown("### Revenue mix — franchise model in action")
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        years_out = [y for y in YEARS if y in FY]
        franchised = [value("is", "Revenues from franchised restaurants", y) for y in years_out]
        company    = [value("is", "Sales by Company-owned and operated restaurants", y) for y in years_out]
        other      = [value("is", "Other revenues", y) for y in years_out]
        fig = bar_chart(
            years_out,
            {"Franchised": franchised, "Company-owned": company, "Other": other},
            y_format="$,.0f", height=320, mode="stack",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        fig = donut_chart(
            ["Franchised", "Company-owned", "Other"],
            [row("is", "Revenues from franchised restaurants")[-1],
             row("is", "Sales by Company-owned and operated restaurants")[-1],
             row("is", "Other revenues")[-1]],
            height=320,
            colors=[GREEN, YELLOW, SOFT_GREY],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    callout(
        "Franchised revenue grew <strong>+5.3%</strong> while company-owned sales declined "
        "slightly. The asset-light, royalty-heavy mix continues to deepen — and so do the margins."
    )


# ─────────────────────────────────────────────────────────────────────
# PAGE 3 — CAPITAL & LIQUIDITY
# ─────────────────────────────────────────────────────────────────────
elif page == "Capital & Liquidity":
    st.markdown("<h1>Capital & Liquidity</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{SUBTLE};font-size:0.95rem;max-width:680px;margin-top:-4px;'>"
        "Solvency, working capital, and the operating-cycle mechanics behind sub-1 liquidity ratios."
        "</p>",
        unsafe_allow_html=True,
    )

    section_divider()

    # ----- KPI strip -----
    cols = st.columns(4, gap="medium")
    metrics = [
        ("Current ratio", fmt_x(row("ratios", "Current ratio")[-1]),
         *fmt_delta(row("ratios", "Current ratio")[-1],
                    row("ratios", "Current ratio")[-2], mode="abs"),
         "Sub-1 by design"),
        ("Net Debt / EBITDA", fmt_x(row("ratios", "Net Debt / EBITDA")[-1]),
         *fmt_delta(row("ratios", "Net Debt / EBITDA")[-1],
                    row("ratios", "Net Debt / EBITDA")[-2], mode="abs", inverse=True),
         "Years of EBITDA"),
        ("Interest coverage", fmt_x(row("ratios", "Interest coverage (EBIT / Interest)")[-1]),
         *fmt_delta(row("ratios", "Interest coverage (EBIT / Interest)")[-1],
                    row("ratios", "Interest coverage (EBIT / Interest)")[-2], mode="abs"),
         "EBIT / Interest"),
        ("Cash Conversion Cycle", fmt_days(row("ratios", "Cash Conversion Cycle (CCC)")[-1]),
         *fmt_delta(row("ratios", "Cash Conversion Cycle (CCC)")[-1],
                    row("ratios", "Cash Conversion Cycle (CCC)")[-2], mode="abs", inverse=True),
         "Negative is great"),
    ]
    for col, m in zip(cols, metrics):
        with col:
            kpi_card(*m)

    section_divider()

    # ----- Liquidity gauges -----
    st.markdown("### Short-term liquidity")
    cols = st.columns(3, gap="large")
    liquidity_ratios = ["Current ratio", "Quick ratio", "Cash ratio"]
    for col, ratio_name in zip(cols, liquidity_ratios):
        with col:
            v = row("ratios", ratio_name)[-1]
            v_prev = row("ratios", ratio_name)[-2]
            b = RATIO_BENCHMARKS[ratio_name]
            st.markdown(
                f"<div class='gauge-label'>{ratio_name}</div>",
                unsafe_allow_html=True,
            )
            fig = bullet_gauge(
                v, b["zones"], b["ideal"],
                value_format="x",
                higher_is_better=b["higher_is_better"], height=110,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            d_txt, d_dir = fmt_delta(v, v_prev, mode="abs")
            arrow = {"up":"▲","down":"▼","neutral":"•"}[d_dir]
            color = {"up":GREEN,"down":DIM_YELLOW,"neutral":SUBTLE}[d_dir]
            st.markdown(
                f"<div class='gauge-delta' style='color:{color};'>"
                f"{arrow}&nbsp;{d_txt} vs FY24</div>",
                unsafe_allow_html=True,
            )

    callout(
        "All three gauges below their textbook ideal — but this is deliberate cash deployment, "
        "not deteriorating operations. <strong>Idle cash fell from $4.6B to $0.8B</strong> as "
        "the surplus was channelled into buybacks and dividends.",
        kind="warn",
    )

    section_divider()

    # ----- Working capital paradox -----
    st.markdown("### The working-capital paradox")
    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        years_out = [y for y in YEARS if y in FY]
        wc  = [value("ratios", "Working Capital ($m)", y) for y in years_out]
        wcn = [value("ratios", "Working Capital Need / WCN ($m)", y) for y in years_out]
        nc  = [value("ratios", "Net Cash position ($m)", y) for y in years_out]

        fig = go.Figure()
        for label, vals, color in [
            ("Working Capital", wc, YELLOW),
            ("WCN (negative = good)", wcn, GREEN),
            ("Net Cash", nc, SOFT_GREY),
        ]:
            fig.add_trace(go.Bar(
                x=years_out, y=vals, name=label,
                marker_color=color, marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>" + label + ": $%{y:,.0f}M<extra></extra>",
            ))
        layout = base_layout(height=340)
        layout["barmode"] = "group"
        layout["bargap"] = 0.35
        layout["xaxis"]["tickmode"] = "array"
        layout["xaxis"]["tickvals"] = years_out
        layout["yaxis"]["tickformat"] = "$,.0f"
        fig.update_layout(**layout)
        fig.add_hline(y=0, line_color=MID_GREY, line_width=1)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        wcn_curr = row("ratios", "Working Capital Need / WCN ($m)")[-1]
        st.markdown(
            f"""
            <div style='padding:10px 0;'>
                <div style='font-size:0.78rem;font-weight:700;color:{YELLOW};
                            letter-spacing:0.18em;text-transform:uppercase;margin-bottom:8px;'>
                    Free float engine
                </div>
                <div style='font-size:2.4rem;font-weight:800;color:{GREEN};
                            line-height:1.1;letter-spacing:-0.02em;'>
                    {fmt_money_m(wcn_curr)}
                </div>
                <div style='color:{OFF_WHITE};font-size:0.92rem;margin-top:4px;'>
                    of permanent, interest-free<br/>supplier financing
                </div>
                <div style='height:1px;background:{MID_GREY};margin:16px 0;'></div>
                <p style='color:{OFF_WHITE};font-size:0.88rem;line-height:1.55;margin:0;'>
                Customers pay instantly via card and app. Inventory turns in a week. Suppliers
                wait 60–75 days. The gap is funded <em>by</em> the operating cycle, not <em>through</em> it.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_divider()

    # ----- CCC decomposition -----
    st.markdown("### Cash Conversion Cycle decomposition")
    years_out = [y for y in YEARS if y in FY]
    dso = [value("ratios", "Days Sales Outstanding (DSO)", y) for y in years_out]
    dio = [value("ratios", "Days Inventory Outstanding (DIO)", y) for y in years_out]
    dpo = [-value("ratios", "Days Payable Outstanding (DPO)", y) for y in years_out]
    ccc = [value("ratios", "Cash Conversion Cycle (CCC)", y) for y in years_out]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="DSO (collecting)", x=years_out, y=dso,
                         marker_color=YELLOW, marker_line_width=0,
                         hovertemplate="<b>%{x}</b><br>DSO: %{y:.1f}d<extra></extra>"))
    fig.add_trace(go.Bar(name="DIO (inventory)", x=years_out, y=dio,
                         marker_color=GREEN, marker_line_width=0,
                         hovertemplate="<b>%{x}</b><br>DIO: %{y:.1f}d<extra></extra>"))
    fig.add_trace(go.Bar(name="−DPO (paying suppliers)", x=years_out, y=dpo,
                         marker_color=DIM_YELLOW, marker_line_width=0,
                         hovertemplate="<b>%{x}</b><br>DPO: %{y:.1f}d<extra></extra>"))
    fig.add_trace(go.Scatter(name="CCC", x=years_out, y=ccc,
                             mode="lines+markers+text",
                             line=dict(color=WHITE, width=3),
                             marker=dict(size=12, color=WHITE,
                                        line=dict(color=BLACK, width=2)),
                             text=[f"{v:.1f}d" for v in ccc],
                             textposition="bottom center",
                             textfont=dict(color=WHITE, size=11, family=PLOTLY_FONT),
                             hovertemplate="<b>%{x}</b><br>CCC: %{y:.1f}d<extra></extra>"))
    layout = base_layout(height=380)
    layout["barmode"] = "relative"
    layout["xaxis"]["tickmode"] = "array"
    layout["xaxis"]["tickvals"] = years_out
    layout["yaxis"]["ticksuffix"] = "d"
    fig.update_layout(**layout)
    fig.add_hline(y=0, line_color=MID_GREY, line_width=1)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    callout(
        "CCC has deepened to <strong>−33 days</strong> in FY25. McDonald's gets paid 33 days "
        "before paying its suppliers — translating directly into the ~$1.8B of free float."
    )

    section_divider()

    # ----- Solvency gauges -----
    st.markdown("### Long-term solvency")
    cols = st.columns(2, gap="large")
    solvency_ratios = ["Interest coverage (EBIT / Interest)", "Net Debt / EBITDA"]
    for col, ratio_name in zip(cols, solvency_ratios):
        with col:
            v = row("ratios", ratio_name)[-1]
            v_prev = row("ratios", ratio_name)[-2]
            b = RATIO_BENCHMARKS[ratio_name]
            st.markdown(
                f"<div class='gauge-label'>{ratio_name}</div>",
                unsafe_allow_html=True,
            )
            fig = bullet_gauge(
                v, b["zones"], b["ideal"],
                value_format="x",
                higher_is_better=b["higher_is_better"], height=110,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            inverse = not b["higher_is_better"]
            d_txt, d_dir = fmt_delta(v, v_prev, mode="abs", inverse=inverse)
            arrow = {"up":"▲","down":"▼","neutral":"•"}[d_dir]
            color = {"up":GREEN,"down":DIM_YELLOW,"neutral":SUBTLE}[d_dir]
            st.markdown(
                f"<div class='gauge-delta' style='color:{color};'>"
                f"{arrow}&nbsp;{d_txt} vs FY24</div>",
                unsafe_allow_html=True,
            )

    callout(
        "<strong>7.8× interest coverage</strong> is fortress-strong. "
        "<strong>Net Debt/EBITDA at 4.4×</strong> is elevated — McDonald's runs more leverage than "
        "typical because royalty cash flows behave more like a REIT than a restaurant chain."
    )


# ─────────────────────────────────────────────────────────────────────
# PAGE 4 — VERDICT
# ─────────────────────────────────────────────────────────────────────
elif page == "Verdict":
    st.markdown("<h1>Verdict</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{SUBTLE};font-size:0.95rem;max-width:660px;margin-top:-4px;'>"
        "Three-year scorecard, strategic synthesis, and the bottom-line take."
        "</p>",
        unsafe_allow_html=True,
    )

    section_divider()

    # ----- Headline number -----
    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        st.markdown(
            f"""
            <div style='padding:6px 0;'>
                <div style='color:{SUBTLE};font-size:0.78rem;font-weight:600;
                            letter-spacing:0.14em;text-transform:uppercase;'>3-Yr Revenue CAGR</div>
                <div style='font-size:2.6rem;font-weight:800;color:{YELLOW};
                            line-height:1.1;'>+2.7%</div>
                <div style='color:{OFF_WHITE};font-size:0.85rem;'>
                    Mature, single-digit growth
                </div>
            </div>
            """, unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div style='padding:6px 0;'>
                <div style='color:{SUBTLE};font-size:0.78rem;font-weight:600;
                            letter-spacing:0.14em;text-transform:uppercase;'>Cumulative FCF (3 yrs)</div>
                <div style='font-size:2.6rem;font-weight:800;color:{GREEN};
                            line-height:1.1;'>$21.1B</div>
                <div style='color:{OFF_WHITE};font-size:0.85rem;'>
                    100%+ of net income
                </div>
            </div>
            """, unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div style='padding:6px 0;'>
                <div style='color:{SUBTLE};font-size:0.78rem;font-weight:600;
                            letter-spacing:0.14em;text-transform:uppercase;'>Cumulative Capital Returned</div>
                <div style='font-size:2.6rem;font-weight:800;color:{YELLOW};
                            line-height:1.1;'>$22.5B</div>
                <div style='color:{OFF_WHITE};font-size:0.85rem;'>
                    Dividends + buybacks
                </div>
            </div>
            """, unsafe_allow_html=True,
        )

    section_divider()

    # ----- Heatmap (the scorecard) -----
    st.markdown("### Three-year ratio heatmap")
    st.markdown(
        f"<p style='color:{SUBTLE};font-size:0.85rem;margin-top:-6px;'>"
        "Cell colour shows change vs FY 2023 (green = improving, dim = deteriorating). "
        "Numbers are the actual ratio values."
        "</p>", unsafe_allow_html=True,
    )

    heat_keys = [
        "Operating margin (EBIT / Revenue)",
        "EBITDA margin",
        "Net margin (Net income / Revenue)",
        "ROCE (NOPAT / Capital Employed)",
        "ROA (Net income / Total assets)",
        "Asset turnover (Revenue / Assets)",
        "Cash Conversion Cycle (CCC)",
        "Current ratio",
        "Quick ratio",
        "Interest coverage (EBIT / Interest)",
        "Net Debt / EBITDA",
        "Dividend payout ratio",
        "P/E ratio",
        "EV / EBITDA",
    ]
    heat_data = {k: row("ratios", k) for k in heat_keys}
    fig = heatmap_matrix(YEARS, heat_data, height=520)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    section_divider()

    # ----- Compact SWOT — plain typographic styling, no decorative symbols -----
    st.markdown("### Strategic synthesis")

    def swot_block(kind, title, items):
        items_html = "".join(
            f"<li><b>{t}</b> — {desc}</li>" for t, desc in items
        )
        return (
            f"<div class='swot {kind}'>"
            f"<h4>{title}</h4>"
            f"<ul>{items_html}</ul>"
            f"</div>"
        )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(
            swot_block("ok", "Strengths", SWOT["strengths"]),
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        st.markdown(
            swot_block("ok", "Opportunities", SWOT["opportunities"]),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            swot_block("warn", "Weaknesses", SWOT["weaknesses"]),
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        st.markdown(
            swot_block("warn", "Threats", SWOT["threats"]),
            unsafe_allow_html=True,
        )

    section_divider()

    # ----- Final verdict (one short paragraph) -----
    st.markdown(
        f"""
        <div style="background:{DARK_GREY};border:1px solid {MID_GREY};
                    border-left:3px solid {GREEN};padding:22px 26px;border-radius:3px;">
            <div style="color:{GREEN};font-size:0.78rem;font-weight:700;
                        letter-spacing:0.18em;text-transform:uppercase;margin-bottom:10px;">
                Final take
            </div>
            <p style="color:{WHITE};font-size:1rem;line-height:1.6;margin:0;">
            Mature, efficient, and shareholder-friendly — executing consistently.
            Flat EV/EBITDA, flat Net Debt/EBITDA, and ~$7B of cash returned each year all signal
            <em>business as usual</em> in the best sense. The textbook ratio toolkit breaks down
            on the equity side; ROCE, Net Debt/EBITDA, FCF yield, and the Cash Conversion Cycle
            are the diagnostics that matter here.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div style='margin-top:28px;color:{SUBTLE};font-size:0.74rem;text-align:center;'>"
        "Built with Streamlit &amp; Plotly · Source: McDonald's 10-K, FY 2023–2025"
        "</div>",
        unsafe_allow_html=True,
    )
