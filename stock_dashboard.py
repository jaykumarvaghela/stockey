"""
╔══════════════════════════════════════════════════════╗
║         NSE STOCK DASHBOARD — Live Tracker           ║
║         Bob (Analyst) + Rob (Dev)  |  2026           ║
╚══════════════════════════════════════════════════════╝

Run with:
    streamlit run stock_dashboard.py

Requirements:
    pip install streamlit yfinance plotly pandas

To add/remove stocks: edit the WATCHLIST dict below.
Format → "Display Name (SYMBOL)": "SYMBOL.NS"
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Dashboard | NSE Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────
#  CUSTOM CSS — Dark Luxury Theme
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: #070b14;
}

.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1400px;
}

/* ── Header ── */
.dash-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    margin-bottom: 2rem;
}
.dash-title {
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
}
.dash-title span {
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.dash-sub {
    color: #475569;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Selector ── */
.stSelectbox label {
    color: #64748b !important;
    font-size: 0.78rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
.stSelectbox > div > div {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 0.8rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
    transition: border-color 0.2s;
}
.stSelectbox > div > div:hover {
    border-color: #38bdf8 !important;
}

/* ── Live Price Hero ── */
.price-hero {
    background: linear-gradient(135deg, #0f172a 0%, #111827 60%, #0f172a 100%);
    border: 1px solid #1e293b;
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    box-shadow: 0 8px 40px rgba(56,189,248,0.06), 0 2px 8px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.price-hero::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(56,189,248,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.price-tag {
    font-size: 0.72rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #475569;
    font-weight: 600;
    margin-bottom: 0.6rem;
}
.price-value {
    font-size: 3.2rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -1.5px;
    line-height: 1;
    font-family: 'DM Mono', monospace !important;
}
.price-change-pos {
    display: inline-block;
    margin-top: 0.7rem;
    background: rgba(16,185,129,0.12);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 8px;
    padding: 0.25rem 0.7rem;
    font-size: 0.95rem;
    font-weight: 600;
    font-family: 'DM Mono', monospace !important;
}
.price-change-neg {
    display: inline-block;
    margin-top: 0.7rem;
    background: rgba(239,68,68,0.12);
    color: #ef4444;
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 8px;
    padding: 0.25rem 0.7rem;
    font-size: 0.95rem;
    font-weight: 600;
    font-family: 'DM Mono', monospace !important;
}
.price-hero-right {
    text-align: right;
}
.prev-close-lbl {
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #334155;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.prev-close-val {
    font-size: 1.3rem;
    color: #64748b;
    font-weight: 600;
    font-family: 'DM Mono', monospace !important;
}

/* ── Section Label ── */
.section-label {
    font-size: 0.7rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #334155;
    font-weight: 700;
    margin: 2rem 0 1rem;
    border-left: 3px solid #38bdf8;
    padding-left: 10px;
}

/* ── Stat Cards ── */
.stat-card {
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.stat-card-lbl {
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    opacity: 0.6;
}
.stat-card-val {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    font-family: 'DM Mono', monospace !important;
    line-height: 1;
}
.card-high {
    background: linear-gradient(135deg, #052e16, #064e3b);
    border: 1px solid rgba(16,185,129,0.2);
    box-shadow: 0 4px 20px rgba(16,185,129,0.08);
    color: #6ee7b7;
}
.card-low {
    background: linear-gradient(135deg, #1c0505, #450a0a);
    border: 1px solid rgba(239,68,68,0.2);
    box-shadow: 0 4px 20px rgba(239,68,68,0.08);
    color: #fca5a5;
}
.card-open {
    background: linear-gradient(135deg, #0d1323, #1e1b4b);
    border: 1px solid rgba(129,140,248,0.2);
    box-shadow: 0 4px 20px rgba(129,140,248,0.08);
    color: #a5b4fc;
}
.card-close {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid rgba(148,163,184,0.15);
    box-shadow: 0 4px 20px rgba(148,163,184,0.05);
    color: #94a3b8;
}

/* ── Volume Card ── */
.volume-card {
    background: linear-gradient(135deg, #0a1628, #0c1e3a);
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 16px;
    padding: 1.4rem 2rem;
    box-shadow: 0 4px 24px rgba(56,189,248,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1rem 0;
}
.vol-left-lbl {
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #38bdf8;
    font-weight: 700;
    opacity: 0.7;
    margin-bottom: 0.4rem;
}
.vol-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #38bdf8;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: -0.5px;
}
.vol-approx {
    font-size: 0.8rem;
    color: #334155;
    margin-top: 0.2rem;
}
.vol-icon { font-size: 2.8rem; opacity: 0.15; }

/* ── History Cards ── */
.hist-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.hist-card-lbl {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #334155;
    font-weight: 700;
    margin-bottom: 0.6rem;
}
.hist-card-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    font-family: 'DM Mono', monospace !important;
}
.hist-card-sub {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 0.3rem;
}
.hist-card-high .hist-card-val { color: #10b981; }
.hist-card-low  .hist-card-val { color: #ef4444; }

/* ── Chart wrapper ── */
.chart-wrap {
    background: #0a0f1e;
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 1rem;
    margin-top: 0.5rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
}

/* ── Footer ── */
.dash-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #1e293b;
    font-size: 0.75rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  WATCHLIST
#  ✏️  Add or remove stocks here freely.
#  Format: "Label (SYMBOL)": "SYMBOL.NS"
#  Use .NS for NSE | .BO for BSE
# ─────────────────────────────────────────────────────────
WATCHLIST = {
    "⚡ Adani Power  (ADANIPOWER)":   "ADANIPOWER.NS",
    "🏗️ Ambuja Cements  (AMBUJACEM)": "AMBUJACEM.NS",
    "🌾 AWL Agri Business  (AWL)":    "AWL.NS",
    # Add more stocks below ↓
    # "🏦 HDFC Bank  (HDFCBANK)":     "HDFCBANK.NS",
    # "💻 Infosys  (INFY)":           "INFY.NS",
}

# ─────────────────────────────────────────────────────────
#  PLOT DEFAULTS
# ─────────────────────────────────────────────────────────
PLOT_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,15,30,0.6)",
    font=dict(family="DM Sans", color="#475569", size=12),
    margin=dict(l=12, r=12, t=16, b=12),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        showgrid=True,
        zeroline=False,
        tickfont=dict(size=11),
        rangeslider=dict(visible=False),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        showgrid=True,
        zeroline=False,
        tickfont=dict(size=11),
        tickprefix="₹",
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#0f172a",
        bordercolor="#1e293b",
        font=dict(color="#e2e8f0", size=12),
    ),
    showlegend=False,
)

# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────
def fmt_price(v):
    return f"₹{v:,.2f}"

def fmt_vol(v):
    if v >= 1e7:   return f"{v/1e7:.2f} Cr"
    elif v >= 1e5: return f"{v/1e5:.2f} L"
    elif v >= 1e3: return f"{v/1e3:.1f} K"
    return f"{v:,.0f}"

@st.cache_data(ttl=300)  # auto-refresh every 5 min
def load_stock_data(ticker: str):
    tk   = yf.Ticker(ticker)
    info = tk.info
    hist = tk.history(period="max", auto_adjust=True)
    hist.index = hist.index.tz_localize(None)
    return info, hist

# ─────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div class="dash-title">📊 <span>Stock</span> Dashboard</div>
    <div class="dash-sub">NSE Live Tracker &nbsp;·&nbsp; Watchlist</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  STOCK SELECTOR
# ─────────────────────────────────────────────────────────
_, col_mid, _ = st.columns([1, 2, 1])
with col_mid:
    chosen = st.selectbox("Select a Stock", list(WATCHLIST.keys()))

ticker = WATCHLIST[chosen]

# ─────────────────────────────────────────────────────────
#  FETCH DATA
# ─────────────────────────────────────────────────────────
with st.spinner("Fetching live market data..."):
    info, hist = load_stock_data(ticker)

if hist.empty:
    st.error("⚠️ Could not load data. Check ticker or internet connection.")
    st.stop()

# ── Derive values ─────────────────────────────────────────
curr_price    = info.get("currentPrice") or info.get("regularMarketPrice") or float(hist["Close"].iloc[-1])
prev_close    = info.get("previousClose") or float(hist["Close"].iloc[-2])
price_chg     = curr_price - prev_close
price_chg_pct = (price_chg / prev_close) * 100

prev         = hist.iloc[-2]
prev_open    = float(prev["Open"])
prev_high    = float(prev["High"])
prev_low     = float(prev["Low"])
prev_close_v = float(prev["Close"])
prev_vol     = int(prev["Volume"])

ath          = float(hist["High"].max())
ath_date     = hist["High"].idxmax().strftime("%d %b %Y")
atl          = float(hist["Low"].min())
atl_date     = hist["Low"].idxmin().strftime("%d %b %Y")
avg_vol      = int(hist["Volume"].mean())

list_date    = hist.index[0].strftime("%d %b %Y")
list_price   = float(hist["Close"].iloc[0])
list_vol     = int(hist["Volume"].iloc[0])

# ─────────────────────────────────────────────────────────
#  LIVE PRICE HERO
# ─────────────────────────────────────────────────────────
badge_cls = "price-change-pos" if price_chg >= 0 else "price-change-neg"
arrow     = "▲" if price_chg >= 0 else "▼"

st.markdown(f"""
<div class="price-hero">
    <div>
        <div class="price-tag">Live Price &nbsp;·&nbsp; NSE</div>
        <div class="price-value">{fmt_price(curr_price)}</div>
        <span class="{badge_cls}">
            {arrow} {fmt_price(abs(price_chg))} &nbsp; ({price_chg_pct:+.2f}%)
        </span>
    </div>
    <div class="price-hero-right">
        <div class="prev-close-lbl">Previous Close</div>
        <div class="prev-close-val">{fmt_price(prev_close)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  PREVIOUS DAY — OHLC CARDS
# ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Previous Day — OHLC</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, cls, lbl, val in [
    (c1, "card-high",  "🔼&nbsp; Prev High",  fmt_price(prev_high)),
    (c2, "card-low",   "🔽&nbsp; Prev Low",   fmt_price(prev_low)),
    (c3, "card-open",  "○&nbsp; Prev Open",   fmt_price(prev_open)),
    (c4, "card-close", "●&nbsp; Prev Close",  fmt_price(prev_close_v)),
]:
    with col:
        st.markdown(f"""
        <div class="stat-card {cls}">
            <div class="stat-card-lbl">{lbl}</div>
            <div class="stat-card-val">{val}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  PREVIOUS DAY — VOLUME
# ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Previous Day — Volume</div>', unsafe_allow_html=True)

vol_vs_avg   = prev_vol / avg_vol if avg_vol else 1
vol_vs_label = f"{'↑' if vol_vs_avg >= 1 else '↓'} {abs(vol_vs_avg - 1)*100:.0f}% vs avg daily volume"

st.markdown(f"""
<div class="volume-card">
    <div>
        <div class="vol-left-lbl">📦 Volume Traded</div>
        <div class="vol-value">{prev_vol:,}</div>
        <div class="vol-approx">{fmt_vol(prev_vol)} shares &nbsp;·&nbsp; {vol_vs_label}</div>
    </div>
    <div class="vol-icon">📦</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  HISTORICAL OVERVIEW CARDS
# ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Historical Overview — Since Listing</div>', unsafe_allow_html=True)

h1, h2, h3, h4 = st.columns(4)
for col, extra_cls, lbl, val, sub in [
    (h1, "",              "📅 Listing Date",  list_date,           "First day on NSE"),
    (h2, "",              "💰 Listing Price", fmt_price(list_price), f"Vol: {fmt_vol(list_vol)}"),
    (h3, "hist-card-high","🏆 All-Time High", fmt_price(ath),      ath_date),
    (h4, "hist-card-low", "📉 All-Time Low",  fmt_price(atl),      atl_date),
]:
    with col:
        st.markdown(f"""
        <div class="hist-card {extra_cls}">
            <div class="hist-card-lbl">{lbl}</div>
            <div class="hist-card-val">{val}</div>
            <div class="hist-card-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  PRICE HISTORY CHART
# ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Price History — All Time</div>', unsafe_allow_html=True)

fig_p = go.Figure()
fig_p.add_trace(go.Scatter(
    x=hist.index, y=hist["Close"],
    mode="lines", name="Close",
    line=dict(color="#38bdf8", width=1.8),
    fill="tozeroy", fillcolor="rgba(56,189,248,0.05)",
    hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.2f}<extra></extra>",
))
fig_p.update_layout(**PLOT_CFG, height=340)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  VOLUME HISTORY CHART
# ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Volume History — All Time</div>', unsafe_allow_html=True)

fig_v = go.Figure()
fig_v.add_trace(go.Bar(
    x=hist.index, y=hist["Volume"],
    name="Volume",
    marker=dict(color="rgba(129,140,248,0.5)", line=dict(color="rgba(129,140,248,0.8)", width=0.4)),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,} shares<extra></extra>",
))
fig_v.update_layout(**{**PLOT_CFG, "yaxis": {**PLOT_CFG["yaxis"], "tickprefix": ""}}, height=260)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-footer">
    Data via Yahoo Finance &nbsp;·&nbsp; Auto-refreshes every 5 min &nbsp;·&nbsp;
    For analysis only, not financial advice &nbsp;·&nbsp;
    Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')} IST
</div>
""", unsafe_allow_html=True)

