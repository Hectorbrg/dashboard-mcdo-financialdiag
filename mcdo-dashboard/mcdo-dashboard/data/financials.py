"""
McDonald's Corporation — FY2023 / FY2024 / FY2025
Financial data extracted from the Excel analysis (units: $ millions unless noted).

Single source of truth for the Streamlit dashboard.
"""

YEARS = [2023, 2024, 2025]

# =========================================================
# INCOME STATEMENT  ($m)
# =========================================================
INCOME_STATEMENT = {
    "Revenues from franchised restaurants":              [15437, 15715, 16548],
    "Sales by Company-owned and operated restaurants":   [9742,  9782,  9690],
    "Other revenues":                                    [316,   423,   647],
    "Total revenues":                                    [25494, 25920, 26885],
    "Franchised restaurants — occupancy expenses":       [2475,  2536,  2618],
    "Food & paper":                                      [3039,  2995,  3006],
    "Payroll & employee benefits":                       [2886,  2959,  2905],
    "Occupancy & other operating expenses":              [2299,  2381,  2358],
    "Other restaurant expenses":                         [232,   339,   564],
    "Depreciation and amortization (SG&A)":              [382,   447,   457],
    "Other SG&A":                                        [2435,  2412,  2583],
    "Other operating (income) expense, net":             [99,    139,   2],
    "Total operating costs and expenses":                [13847, 14208, 14492],
    "Operating income (EBIT)":                           [11647, 11712, 12393],
    "Interest expense, net":                             [1361,  1506,  1582],
    "Nonoperating (income) expense, net":                [-236,  -139,  -87],
    "Income before income taxes":                        [10522, 10345, 10897],
    "Provision for income taxes":                        [2053,  2121,  2334],
    "Net income":                                        [8469,  8223,  8563],
    # Per-share data
    "EPS — basic ($)":                                   [11.63, 11.45, 12.00],
    "EPS — diluted ($)":                                 [11.56, 11.39, 11.95],
    "Dividends declared per share ($)":                  [6.23,  6.78,  7.17],
    "Weighted-avg shares basic (m)":                     [727.9, 718.3, 713.4],
    "Weighted-avg shares diluted (m)":                   [732.3, 721.9, 716.4],
}

# =========================================================
# BALANCE SHEET  ($m)
# =========================================================
BALANCE_SHEET = {
    # Current assets
    "Cash and equivalents":                              [4579, 1085, 774],
    "Accounts and notes receivable":                     [2488, 2383, 2466],
    "Inventories, at cost":                              [53,   56,   61],
    "Prepaid expenses and other current assets":         [866,  1074, 863],
    "Total current assets":                              [7986, 4599, 4163],
    # Non-current assets
    "Investments in and advances to affiliates":         [1080, 2710, 2820],
    "Goodwill":                                          [3040, 3145, 3354],
    "Miscellaneous other assets":                        [5618, 6095, 6331],
    "Total other assets":                                [9738, 11950, 12505],
    "Lease right-of-use asset, net":                     [13514, 13339, 14606],
    "Property and equipment, at cost":                   [43570, 44177, 49290],
    "Accumulated depreciation":                          [-18662, -18882, -21049],
    "Net property and equipment":                        [24908, 25295, 28241],
    "Total assets":                                      [56147, 55182, 59515],
    # Current liabilities
    "Short-term borrowings & current LT debt":           [2192, 0,    0],
    "Accounts payable":                                  [1103, 1029, 1149],
    "Current lease liability":                           [688,  636,  694],
    "Income taxes (current)":                            [705,  361,  250],
    "Other taxes (current)":                             [268,  224,  247],
    "Accrued interest":                                  [469,  482,  533],
    "Accrued payroll and other liabilities":             [1434, 1129, 1488],
    "Total current liabilities":                         [6859, 3861, 4361],
    # Non-current liabilities
    "Long-term debt":                                    [37153, 38424, 39973],
    "Long-term lease liability":                         [13058, 12888, 14147],
    "Long-term income taxes":                            [363,   344,   139],
    "Deferred revenues — initial franchise fees":        [790,   778,   945],
    "Other long-term liabilities":                       [950,   771,   704],
    "Deferred income taxes":                             [1681,  1914,  1038],
    # Equity
    "Common stock":                                      [17,    17,    17],
    "Additional paid-in capital":                        [8893,  9281,  9641],
    "Retained earnings":                                 [63480, 66834, 70282],
    "Accumulated other comprehensive income (loss)":     [-2456, -2553, -2414],
    "Common stock in treasury, at cost":                 [-74640, -77375, -79316],
    "Total shareholders' equity (deficit)":              [-4707, -3797, -1791],
    "Total liabilities and equity":                      [56147, 55182, 59515],
}

# =========================================================
# CASH FLOW STATEMENT  ($m)
# =========================================================
CASH_FLOW = {
    "Net income":                                        [8469, 8223, 8563],
    "Depreciation and amortization (CFS)":               [1978, 2097, 2199],
    "Cash provided by operations (CFO)":                 [9612, 9447, 10551],
    "Capital expenditures":                              [-2357, -2775, -3365],
    "Cash used for investing (CFI)":                     [-3185, -5346, -3822],
    "Treasury stock purchases":                          [-3054, -2824, -2056],
    "Common stock dividends":                            [-4533, -4870, -5115],
    "Long-term financing issuances":                     [5221,  2380,  4724],
    "Long-term financing repayments":                    [-2441, -2777, -4802],
    "Cash used for financing (CFF)":                     [-4374, -7495, -7125],
    "Free Cash Flow (CFO - CapEx)":                      [7255, 6672, 7186],
    "Cash Conversion Ratio (CFO/NI)":                    [1.135, 1.149, 1.232],
}

# =========================================================
# RATIOS  (computed in spreadsheet — verified)
# 2023 values computed here from raw data; 2024 & 2025 match the file.
# =========================================================
RATIOS = {
    # ---- Profitability (Operating-management view) ----
    "Operating margin (EBIT / Revenue)":     [0.4569, 0.4519, 0.4610],
    "EBITDA margin":                         [0.4719, 0.4691, 0.4780],
    "Net margin (Net income / Revenue)":     [0.3322, 0.3172, 0.3185],
    "EBITDA ($m)":                           [12029, 12159, 12850],
    # ---- Returns ----
    "ROCE (NOPAT / Capital Employed)":       [None,   0.1602, 0.1553],   # 2023 not in file
    "ROA (Net income / Total assets)":       [0.1508, 0.1490, 0.1439],
    "ROE (meaningless — neg. equity)":       [None,   -2.166, -4.781],   # flagged meaningless
    # ---- Efficiency / Activity ----
    "Asset turnover (Revenue / Assets)":     [0.4541, 0.4697, 0.4517],
    "Days Sales Outstanding (DSO)":          [35.62,  33.10,  33.02],
    "Days Inventory Outstanding (DIO)":      [6.36,   6.73,   7.31],
    "Days Payable Outstanding (DPO)":        [62.61,  66.98,  73.55],
    "Cash Conversion Cycle (CCC)":           [-20.63, -27.15, -33.22],
    "PP&E turnover":                         [None,   1.025,  0.952],    # uses 2-year avg
    # ---- Liquidity ----
    "Current ratio":                         [1.164,  1.191,  0.955],
    "Quick ratio":                           [1.156,  1.177,  0.941],
    "Cash ratio":                            [0.668,  0.281,  0.177],
    # ---- Solvency / Leverage ----
    "Total debt ratio (TL / TA)":            [1.084,  1.139,  1.103],
    "Interest coverage (EBIT / Interest)":   [8.558,  7.777,  7.834],
    "Net Debt / EBITDA":                     [3.882,  4.137,  4.432],
    "Net Debt ($m)":                         [46690,  51892,  55189],
    # ---- Investor / Valuation ----
    "Dividend payout ratio":                 [0.5354, 0.5922, 0.5973],
    "Dividend yield":                        [0.0213, 0.0235, 0.0235],
    "P/E ratio":                             [25.17,  25.06,  25.38],
    "Closing share price ($)":               [292.93, 288.23, 305.63],
    "Market capitalization ($m)":            [211789, 206082, 217303],
    "Enterprise Value ($m)":                 [258479, 257976, 272492],
    "EV / EBITDA":                           [21.49,  18.68,  18.67],
    # ---- Working capital structure ----
    "Working Capital ($m)":                  [1127,   738,   -198],
    "Working Capital Need / WCN ($m)":       [-1007,  -1421, -1835],
    "Net Cash position ($m)":                [2387,   2159,  1638],
    "Capital Employed ($m)":                 [44799,  49162, 53517],
    "Invested Capital ($m)":                 [42446,  48095, 53398],
}

# Benchmark zones for gauge / bullet charts.  Format: (low_red, low_yellow, healthy_low, healthy_high)
# Higher = better (e.g., Current ratio): zones go red→yellow→green left→right
# Lower = better (e.g., Net Debt/EBITDA): inverted; we handle in the chart helper.
RATIO_BENCHMARKS = {
    "Current ratio":        {"zones": [0, 1.0, 1.5, 2.5], "ideal": (1.5, 2.0), "higher_is_better": True,
                             "definition": "Current assets divided by current liabilities — measures the ability to cover short-term obligations with short-term resources.",
                             "why":        "Below 1 means more bills due than cash & receivables on hand. For most companies this is a warning. For McDonald's, the operating cycle generates cash so this ratio reads differently.",
                             "mcdo":       "Sub-1 here is a feature, not a bug: customers pay instantly while suppliers wait 60+ days. The 'liability' is interest-free supplier float, not debt."},
    "Quick ratio":          {"zones": [0, 0.5, 1.0, 2.0], "ideal": (1.0, 1.5), "higher_is_better": True,
                             "definition": "(Cash + receivables) ÷ current liabilities — same as current ratio but excludes inventory.",
                             "why":        "Tests whether a company can pay its short-term bills without selling inventory.",
                             "mcdo":       "Inventory is irrelevant for McDonald's (turns in 7 days), so quick ≈ current ratio. Same operational-cash story."},
    "Cash ratio":           {"zones": [0, 0.2, 0.5, 1.0], "ideal": (0.3, 0.5), "higher_is_better": True,
                             "definition": "Cash & equivalents ÷ current liabilities.",
                             "why":        "Most conservative liquidity test — only counts cash on hand.",
                             "mcdo":       "Has dropped sharply (0.67 → 0.18) as McDonald's deliberately deployed idle cash into buybacks and dividends. Capital discipline, not distress."},
    "Interest coverage (EBIT / Interest)": {"zones": [0, 1.5, 3.0, 8.0], "ideal": (5.0, 10.0), "higher_is_better": True,
                             "definition": "Operating income ÷ interest expense — how many times over the company can pay its interest bill.",
                             "why":        "Below 3 is concerning. Above 5 is comfortable. Above 8 is fortress-like.",
                             "mcdo":       "At ~7.8×, comfortably investment-grade. Operating income is 8× the interest bill — debt service is a non-issue."},
    "Net Debt / EBITDA":    {"zones": [0, 1.5, 3.0, 5.0], "ideal": (2.0, 3.0), "higher_is_better": False,
                             "definition": "Net debt (debt minus cash) divided by EBITDA — years of earnings needed to repay all debt.",
                             "why":        "Below 2× = conservative. 2–3× = healthy. Above 4× = elevated leverage.",
                             "mcdo":       "At 4.4×, on the higher side — but McDonald's runs this profile deliberately. Stable rents-like franchise revenue can support more leverage than typical companies."},
    "Total debt ratio (TL / TA)": {"zones": [0, 0.4, 0.7, 1.2], "ideal": (0.4, 0.7), "higher_is_better": False,
                             "definition": "Total liabilities ÷ total assets.",
                             "why":        "Below 0.5 = conservative. 0.5–0.7 = normal. Above 1 means liabilities exceed assets (negative equity).",
                             "mcdo":       "Above 1.0 because of negative equity from buybacks. Mathematically stressful, economically irrelevant — the buybacks are a return of capital, not a balance-sheet risk."},
    "Operating margin (EBIT / Revenue)": {"zones": [0, 0.10, 0.25, 0.50], "ideal": (0.30, 0.50), "higher_is_better": True,
                             "definition": "Operating income as a percentage of revenue.",
                             "why":        "Measures how much of every revenue dollar becomes operating profit. Industry-leading restaurants run 15–25%.",
                             "mcdo":       "At 46% McDonald's is in a different league. The franchise model captures royalties on system-wide sales without the cost base — almost pure margin."},
    "Net margin (Net income / Revenue)": {"zones": [0, 0.05, 0.15, 0.35], "ideal": (0.20, 0.35), "higher_is_better": True,
                             "definition": "Net income as a percentage of revenue.",
                             "why":        "Bottom-line profitability after all costs, interest, and taxes.",
                             "mcdo":       "32% net margin is exceptional. Even after $1.6B in interest expense and 21% effective tax, McDonald's keeps 32¢ of every revenue dollar."},
    "EBITDA margin":        {"zones": [0, 0.15, 0.30, 0.55], "ideal": (0.35, 0.55), "higher_is_better": True,
                             "definition": "EBITDA as a percentage of revenue.",
                             "why":        "Measures cash-flow profitability before financing and accounting choices.",
                             "mcdo":       "48% EBITDA margin reflects the franchise-fee economics: receive 4–5% royalty on franchisee sales with almost no cost."},
    "ROCE (NOPAT / Capital Employed)": {"zones": [0, 0.08, 0.15, 0.25], "ideal": (0.15, 0.25), "higher_is_better": True,
                             "definition": "Net operating profit after tax ÷ capital employed (equity + long-term debt).",
                             "why":        "Measures how efficiently a company turns total invested capital into operating profit. Best return metric when equity is distorted by buybacks.",
                             "mcdo":       "16% ROCE is excellent, especially compared to McDonald's weighted cost of capital (~7%). Every dollar of capital earns ~9 percentage points above its cost."},
    "ROA (Net income / Total assets)": {"zones": [0, 0.05, 0.10, 0.20], "ideal": (0.10, 0.20), "higher_is_better": True,
                             "definition": "Net income ÷ total assets — profitability per dollar of asset.",
                             "why":        "An equity-neutral profitability metric.",
                             "mcdo":       "14% ROA: McDonald's earns 14¢ of net income per dollar of assets, well above the restaurant-industry average."},
    "Cash Conversion Cycle (CCC)": {"zones": [-50, -10, 30, 90], "ideal": (-50, 0), "higher_is_better": False,
                             "definition": "DSO + DIO − DPO. Number of days between paying suppliers and collecting from customers.",
                             "why":        "Negative means suppliers finance the business. Most companies are positive (15–60 days). Negative is the gold standard.",
                             "mcdo":       "−33 days. McDonald's gets paid by customers 33 days before paying suppliers. Translates to ~$1.8B of permanent, interest-free working capital."},
    "Asset turnover (Revenue / Assets)": {"zones": [0, 0.3, 0.6, 1.2], "ideal": (0.5, 1.0), "higher_is_better": True,
                             "definition": "Revenue ÷ total assets — sales generated per dollar of assets.",
                             "why":        "Measures asset productivity. Capital-light businesses run higher ratios.",
                             "mcdo":       "0.45 — typical for a real-estate-heavy QSR. Land and buildings sit on the balance sheet; the franchisees use them."},
    "Dividend payout ratio": {"zones": [0, 0.20, 0.50, 0.80], "ideal": (0.40, 0.60), "higher_is_better": True,
                             "definition": "Dividends paid per share ÷ EPS.",
                             "why":        "Measures the share of profits returned as dividends. Mature companies sit at 40–60%.",
                             "mcdo":       "60% payout — squarely in the 'mature dividend payer' band. Consistent annual dividend hikes since 1976."},
    "EV / EBITDA":          {"zones": [5, 12, 20, 30], "ideal": (12, 20), "higher_is_better": False,
                             "definition": "Enterprise value ÷ EBITDA — capital-structure-neutral valuation multiple.",
                             "why":        "Higher = more expensive. Restaurants typically trade 10–18×.",
                             "mcdo":       "18.7× — premium valuation reflecting brand strength, defensive cash flows, and long dividend history."},
}

# =========================================================
# NARRATIVE BLOCKS — written by the analyst, used in the dashboard
# =========================================================
NARRATIVES = {
    "executive_verdict": (
        "McDonald's enters FY2025 in textbook shape for a mature, capital-return franchise. Revenue grew 3.7% to "
        "$26.9B, operating margin expanded to 46.1%, and free cash flow held above $7B. The headline ratios that "
        "look uncomfortable — current ratio below 1, debt-to-equity off the chart, negative book equity — are not "
        "warning signs but the mechanical signature of a capital-light franchise running aggressive buybacks. "
        "Strip out those distortions and what remains is a 32% net-margin business converting >100% of earnings to "
        "cash, returning $7B+ to shareholders annually, and growing its EPS through both operational gains and "
        "share count reduction."
    ),
    "wcn_paradox": (
        "McDonald's runs a deeply negative Working Capital Need ($-1.8B), meaning suppliers and customers are net "
        "lenders to the business. Customers pay instantly via card and app; inventory turns in roughly a week; "
        "suppliers are paid 60–75 days later. This 33-day cash-conversion gap translates to ~$1.8B of permanent, "
        "interest-free financing. For most companies, a current ratio below 1 is a red flag. For a QSR with a "
        "deeply negative WCN, sub-1 liquidity ratios are the optimal balance-sheet configuration — every dollar of "
        "float is deployed elsewhere instead of sitting idle in working capital."
    ),
    "negative_equity": (
        "Book equity is negative (-$1.8B) because cumulative share buybacks ($79.3B in treasury stock) exceed "
        "retained earnings ($70.3B). This is not financial distress — it is the exact opposite. Over time "
        "McDonald's earned more than it needed to reinvest, so it returned the surplus to shareholders. The "
        "consequence is that any equity-based ratio (ROE, Debt/Equity, P/B, Equity Multiplier) is mathematically "
        "meaningless. ROCE replaces ROE; total-debt-to-EBITDA replaces D/E."
    ),
    "final_verdict": (
        "This is the profile of a mature, efficient, shareholder-friendly business executing consistently. No "
        "surprises in either direction — and for a company of McDonald's quality, consistency is the headline. A "
        "flat EV/EBITDA and flat Net Debt/EBITDA signal 'business as usual' in the best sense: the company "
        "continues to do what it has always done, and the market continues to reward it accordingly."
    ),
}

# SWOT-style synthesis
SWOT = {
    "strengths": [
        ("Industry-leading margins", "46% operating margin and 48% EBITDA margin reflect the royalty-heavy franchise model — best-in-class economics."),
        ("Cash generation machine", "FCF stable at ~$7B/yr, CFO/NI conversion of 1.23× shows accounting earnings translate efficiently to cash."),
        ("Negative working capital need", "-$1.8B of interest-free financing extracted from the operating cycle; CCC of -33 days."),
        ("Capital return discipline", "$7B+ annually returned to shareholders via dividends + buybacks — payout ratio near 60% with consistent dividend growth."),
        ("Defensive interest coverage", "EBIT covers interest 7.8×, comfortably investment-grade despite high absolute leverage."),
    ],
    "weaknesses": [
        ("Negative book equity", "Treasury stock ($79B) exceeds retained earnings ($70B) — distorts every equity-based ratio. Optical issue, not economic."),
        ("Elevated leverage", "Net Debt/EBITDA at 4.4× is on the higher side; not dangerous given franchise stability but limits flexibility."),
        ("Cash buffer thinning", "Cash dropped from $4.6B (2023) to $0.8B (2025) as buybacks and dividends absorbed liquidity. Healthy if FCF stays strong."),
        ("Modest top-line growth", "3.7% revenue growth in 2025 — solid but not exciting; relies on pricing and franchise fees more than unit growth."),
    ],
    "opportunities": [
        ("Digital/loyalty acceleration", "Rising 'other revenues' (+53%) suggests app, delivery, and tech monetization gaining traction."),
        ("International expansion", "Developmental Licensee model still has runway in emerging markets with low capital intensity."),
        ("Continued buyback yield", "At ~25× P/E, mechanical EPS growth of ~1% per year just from share count reduction."),
    ],
    "threats": [
        ("Consumer pressure on QSR", "Inflation-fatigued consumers may trade down or out; 2024 already saw flat real growth."),
        ("Franchisee health", "Royalty model only works if operators stay profitable. Rising interest rates squeeze franchisee economics."),
        ("Regulatory/tax exposure", "Global QSR scale invites scrutiny — labor laws, sugar/health regulation, and minimum tax frameworks."),
    ],
}
