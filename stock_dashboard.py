"""
╔══════════════════════════════════════════════════════╗
║      NSE STOCK DASHBOARD v2 — Live Tracker           ║
║      Bob (Analyst) + Rob (Dev)  |  2026              ║
╚══════════════════════════════════════════════════════╝

Run:   streamlit run stock_dashboard.py
Deps:  pip install -r requirements.txt

WATCHLIST: edit the dict below to add/remove any stock.
Format → "Label": "SYMBOL.NS"
"""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Dashboard | NSE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────
#  STYLES
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #070b14; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px; }

/* ── Header ── */
.dash-header { text-align:center; padding:2rem 0 1rem; margin-bottom:1.5rem; }
.dash-title  { font-size:2.4rem; font-weight:700; letter-spacing:-1px; color:#f1f5f9; margin-bottom:.3rem; }
.dash-title span { background:linear-gradient(90deg,#38bdf8,#818cf8,#c084fc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.dash-sub    { color:#334155; font-size:.85rem; letter-spacing:2.5px; text-transform:uppercase; font-weight:500; }

/* ── Stock selector: pill-style segmented control ── */
div[data-testid="stSegmentedControl"] > div {
    background: #0d1424 !important;
    border: 1px solid #1e293b !important;
    border-radius: 50px !important;
    padding: 4px !important;
    gap: 4px !important;
}
div[data-testid="stSegmentedControl"] button {
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-size: .92rem !important;
    color: #475569 !important;
    padding: .45rem 1.4rem !important;
    transition: all .2s !important;
    border: none !important;
}
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background: linear-gradient(135deg,#1d4ed8,#7c3aed) !important;
    color: #fff !important;
    box-shadow: 0 2px 12px rgba(99,102,241,.35) !important;
}
div[data-testid="stSegmentedControl"] button:hover {
    color: #e2e8f0 !important;
}
div[data-testid="stSegmentedControl"] label { display:none !important; }

/* ── Timeframe radio ── */
div[data-testid="stRadio"] > div {
    flex-direction:row !important; gap:6px !important;
    flex-wrap:wrap !important;
}
div[data-testid="stRadio"] label {
    background:#0f172a; border:1px solid #1e293b; border-radius:50px;
    padding:.3rem 1rem; cursor:pointer; transition:all .2s;
    color:#475569; font-weight:600; font-size:.82rem;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background:linear-gradient(135deg,#0ea5e9,#6366f1);
    border-color:transparent; color:#fff;
    box-shadow:0 2px 10px rgba(56,189,248,.25);
}
div[data-testid="stRadio"] input[type=radio] { display:none; }
div[data-testid="stRadio"] > label { display:none !important; }

/* ── Section label ── */
.section-label {
    font-size:.68rem; letter-spacing:2.5px; text-transform:uppercase;
    color:#334155; font-weight:700; margin:1.8rem 0 .9rem;
    border-left:3px solid #38bdf8; padding-left:10px;
}

/* ── Live price hero ── */
.price-hero {
    background:linear-gradient(135deg,#0f172a 0%,#111827 60%,#0f172a 100%);
    border:1px solid #1e293b; border-radius:20px; padding:2rem 2.5rem;
    box-shadow:0 8px 40px rgba(56,189,248,.06);
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:1.4rem; position:relative; overflow:hidden;
}
.price-hero::before {
    content:''; position:absolute; top:-60px; left:-60px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(56,189,248,.06) 0%,transparent 70%);
    border-radius:50%;
}
.price-tag   { font-size:.7rem; letter-spacing:2px; text-transform:uppercase; color:#475569; font-weight:600; margin-bottom:.5rem; }
.price-value { font-size:3rem; font-weight:700; color:#f1f5f9; letter-spacing:-1.5px; line-height:1; font-family:'DM Mono',monospace !important; }
.price-change-pos { display:inline-block; margin-top:.6rem; background:rgba(16,185,129,.12); color:#10b981; border:1px solid rgba(16,185,129,.25); border-radius:8px; padding:.2rem .65rem; font-size:.92rem; font-weight:600; font-family:'DM Mono',monospace !important; }
.price-change-neg { display:inline-block; margin-top:.6rem; background:rgba(239,68,68,.12); color:#ef4444; border:1px solid rgba(239,68,68,.25); border-radius:8px; padding:.2rem .65rem; font-size:.92rem; font-weight:600; font-family:'DM Mono',monospace !important; }
.prev-close-lbl { font-size:.7rem; letter-spacing:1.5px; text-transform:uppercase; color:#334155; font-weight:600; margin-bottom:.3rem; text-align:right; }
.prev-close-val { font-size:1.25rem; color:#64748b; font-weight:600; font-family:'DM Mono',monospace !important; text-align:right; }

/* ── OHLC stat cards ── */
.stat-card { border-radius:16px; padding:1.3rem 1.4rem; height:105px; display:flex; flex-direction:column; justify-content:space-between; }
.stat-card-lbl { font-size:.66rem; letter-spacing:2px; text-transform:uppercase; font-weight:700; opacity:.6; }
.stat-card-val { font-size:1.5rem; font-weight:700; letter-spacing:-.5px; font-family:'DM Mono',monospace !important; line-height:1; }
.card-high  { background:linear-gradient(135deg,#052e16,#064e3b); border:1px solid rgba(16,185,129,.2);  box-shadow:0 4px 20px rgba(16,185,129,.08);  color:#6ee7b7; }
.card-low   { background:linear-gradient(135deg,#1c0505,#450a0a); border:1px solid rgba(239,68,68,.2);   box-shadow:0 4px 20px rgba(239,68,68,.08);   color:#fca5a5; }
.card-open  { background:linear-gradient(135deg,#0d1323,#1e1b4b); border:1px solid rgba(129,140,248,.2); box-shadow:0 4px 20px rgba(129,140,248,.08); color:#a5b4fc; }
.card-close { background:linear-gradient(135deg,#111827,#1f2937); border:1px solid rgba(148,163,184,.15);box-shadow:0 4px 20px rgba(148,163,184,.05);color:#94a3b8; }

/* ── Volume card ── */
.volume-card {
    background:linear-gradient(135deg,#0a1628,#0c1e3a);
    border:1px solid rgba(56,189,248,.18); border-radius:16px;
    padding:1.3rem 1.8rem; box-shadow:0 4px 24px rgba(56,189,248,.07);
    margin:.8rem 0;
}
.vol-title { font-size:.68rem; letter-spacing:2px; text-transform:uppercase; color:#38bdf8; font-weight:700; opacity:.7; margin-bottom:.4rem; }
.vol-total { font-size:1.8rem; font-weight:700; color:#38bdf8; font-family:'DM Mono',monospace !important; letter-spacing:-.5px; }
.vol-sub   { font-size:.78rem; color:#334155; margin-top:.2rem; }

/* ── History cards ── */
.hist-card { background:#0f172a; border:1px solid #1e293b; border-radius:16px; padding:1.3rem 1.4rem; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,.3); }
.hist-card-lbl { font-size:.63rem; letter-spacing:2px; text-transform:uppercase; color:#334155; font-weight:700; margin-bottom:.5rem; }
.hist-card-val { font-size:1.1rem; font-weight:700; color:#e2e8f0; font-family:'DM Mono',monospace !important; }
.hist-card-sub { font-size:.7rem; color:#475569; margin-top:.3rem; }
.hist-card-high .hist-card-val { color:#10b981; }
.hist-card-low  .hist-card-val { color:#ef4444; }

/* ── Chart wrapper ── */
.chart-wrap { background:#0a0f1e; border:1px solid #1e293b; border-radius:18px; padding:1rem; margin-top:.4rem; box-shadow:0 4px 30px rgba(0,0,0,.4); }

/* ── Footer ── */
.dash-footer { text-align:center; padding:2rem 0 1rem; color:#1e293b; font-size:.72rem; letter-spacing:.5px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  WATCHLIST  — edit freely
# ─────────────────────────────────────────────────────
WATCHLIST = {
    "⚡ Adani Power":      "ADANIPOWER.NS",
    "🏗️ Ambuja Cements":  "AMBUJACEM.NS",
    "🌾 AWL Agri Business": "AWL.NS",
    # Add more ↓
    # "🏦 HDFC Bank":    "HDFCBANK.NS",
}

TIMEFRAMES = {
    "1M": "1mo", "3M": "3mo", "6M": "6mo",
    "1Y": "1y",  "3Y": "3y",  "5Y": "5y", "All": "max",
}

PLOT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,15,30,0.6)",
    font=dict(family="DM Sans", color="#475569", size=12),
    margin=dict(l=12, r=12, t=16, b=12),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", showgrid=True, zeroline=False, rangeslider=dict(visible=False)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", showgrid=True, zeroline=False, tickprefix="₹"),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#0f172a", bordercolor="#1e293b", font=dict(color="#e2e8f0", size=12)),
    showlegend=False,
)

# ─────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────
def fmt_price(v):       return f"₹{v:,.2f}"
def fmt_vol(v):
    if v >= 1e7:        return f"{v/1e7:.2f} Cr"
    elif v >= 1e5:      return f"{v/1e5:.2f} L"
    elif v >= 1e3:      return f"{v/1e3:.1f} K"
    return f"{v:,.0f}"

def buy_sell_estimate(row):
    """
    Estimate buy/sell volume split using price position within the bar.
    Buy pressure = (Close - Low) / (High - Low)  — money flow logic.
    """
    h, l, c, v = float(row["High"]), float(row["Low"]), float(row["Close"]), int(row["Volume"])
    rng = h - l
    buy_pct = ((c - l) / rng) if rng > 0 else 0.5
    return int(v * buy_pct), int(v * (1 - buy_pct))

def vol_bar_html(buy_vol, sell_vol):
    total = buy_vol + sell_vol or 1
    buy_pct  = int(buy_vol  / total * 100)
    sell_pct = 100 - buy_pct
    return f"""
    <div style="margin-top:.8rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
            <span style="color:#10b981; font-size:.78rem; font-weight:600;">🟢 Buy {buy_pct}% &nbsp; {fmt_vol(buy_vol)}</span>
            <span style="color:#ef4444;  font-size:.78rem; font-weight:600;">{fmt_vol(sell_vol)} &nbsp; {sell_pct}% Sell 🔴</span>
        </div>
        <div style="background:#1e293b; border-radius:6px; height:8px; overflow:hidden;">
            <div style="background:linear-gradient(90deg,#10b981,#34d399); width:{buy_pct}%; height:100%;"></div>
        </div>
    </div>"""

@st.cache_data(ttl=300)
def load_full_history(ticker: str):
    tk   = yf.Ticker(ticker)
    info = tk.info
    hist = tk.history(period="max", auto_adjust=True)
    hist.index = hist.index.tz_localize(None)
    return info, hist

@st.cache_data(ttl=300)
def load_period(ticker: str, period: str):
    h = yf.Ticker(ticker).history(period=period, auto_adjust=True)
    h.index = h.index.tz_localize(None)
    return h

# ─────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div class="dash-title">📊 <span>Stock</span> Dashboard</div>
    <div class="dash-sub">NSE Live Tracker &nbsp;·&nbsp; Watchlist</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  STOCK SELECTOR — pill segmented control
# ─────────────────────────────────────────────────────
_, mid, _ = st.columns([1, 3, 1])
with mid:
    chosen = st.segmented_control(
        "stock_selector",
        options=list(WATCHLIST.keys()),
        default=list(WATCHLIST.keys())[0],
        label_visibility="hidden",
        key="stock_seg",
    )
if chosen is None:
    chosen = list(WATCHLIST.keys())[0]

ticker = WATCHLIST[chosen]

# ─────────────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────────────
with st.spinner("Loading market data..."):
    info, hist = load_full_history(ticker)

if hist.empty:
    st.error("⚠️ Could not load data.")
    st.stop()

# Store for fragment
st.session_state["_ticker"] = ticker
st.session_state["_prev_close"] = info.get("previousClose") or float(hist["Close"].iloc[-2])

# ─────────────────────────────────────────────────────
#  LIVE PRICE — refreshes every 3 seconds
# ─────────────────────────────────────────────────────
@st.fragment(run_every=3)
def live_price_card():
    _ticker     = st.session_state.get("_ticker", "")
    _prev_close = st.session_state.get("_prev_close", 0)
    try:
        fresh = yf.Ticker(_ticker).info
        curr  = fresh.get("currentPrice") or fresh.get("regularMarketPrice") or float(hist["Close"].iloc[-1])
    except Exception:
        curr  = float(hist["Close"].iloc[-1])

    chg     = curr - _prev_close
    chg_pct = (chg / _prev_close * 100) if _prev_close else 0
    badge   = "price-change-pos" if chg >= 0 else "price-change-neg"
    arrow   = "▲" if chg >= 0 else "▼"
    ts      = datetime.now().strftime("%H:%M:%S")

    st.markdown(f"""
    <div class="price-hero">
        <div>
            <div class="price-tag">Live Price &nbsp;·&nbsp; NSE &nbsp;·&nbsp;
                <span style="color:#1e3a5f; font-family:'DM Mono',monospace;">{ts}</span>
            </div>
            <div class="price-value">{fmt_price(curr)}</div>
            <span class="{badge}">{arrow} {fmt_price(abs(chg))} &nbsp;({chg_pct:+.2f}%)</span>
        </div>
        <div>
            <div class="prev-close-lbl">Previous Close</div>
            <div class="prev-close-val">{fmt_price(_prev_close)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

live_price_card()

# ─────────────────────────────────────────────────────
#  TODAY — CURRENT SESSION
# ─────────────────────────────────────────────────────
today     = hist.iloc[-1]
t_buy, t_sell = buy_sell_estimate(today)
t_vol     = int(today["Volume"])

st.markdown('<div class="section-label">Today — Current Session</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
for col, cls, lbl, val in [
    (c1, "card-high",  "🔼 Day High",  fmt_price(float(today["High"]))),
    (c2, "card-low",   "🔽 Day Low",   fmt_price(float(today["Low"]))),
    (c3, "card-open",  "○ Day Open",   fmt_price(float(today["Open"]))),
    (c4, "card-close", "● Day Close",  fmt_price(float(today["Close"]))),
]:
    with col:
        st.markdown(f'<div class="stat-card {cls}"><div class="stat-card-lbl">{lbl}</div><div class="stat-card-val">{val}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="volume-card">
    <div class="vol-title">📦 Today Volume</div>
    <div class="vol-total">{t_vol:,}</div>
    <div class="vol-sub">{fmt_vol(t_vol)} shares</div>
    {vol_bar_html(t_buy, t_sell)}
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  PREVIOUS DAY — OHLC + VOLUME
# ─────────────────────────────────────────────────────
prev         = hist.iloc[-2]
p_buy, p_sell = buy_sell_estimate(prev)
p_vol        = int(prev["Volume"])
avg_vol      = int(hist["Volume"].mean())
vol_ratio    = p_vol / avg_vol if avg_vol else 1
vol_vs       = f"{'↑' if vol_ratio >= 1 else '↓'} {abs(vol_ratio-1)*100:.0f}% vs avg daily"

st.markdown('<div class="section-label">Previous Day — OHLC</div>', unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)
for col, cls, lbl, val in [
    (p1, "card-high",  "🔼 Prev High",  fmt_price(float(prev["High"]))),
    (p2, "card-low",   "🔽 Prev Low",   fmt_price(float(prev["Low"]))),
    (p3, "card-open",  "○ Prev Open",   fmt_price(float(prev["Open"]))),
    (p4, "card-close", "● Prev Close",  fmt_price(float(prev["Close"]))),
]:
    with col:
        st.markdown(f'<div class="stat-card {cls}"><div class="stat-card-lbl">{lbl}</div><div class="stat-card-val">{val}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="volume-card">
    <div class="vol-title">📦 Previous Day Volume</div>
    <div class="vol-total">{p_vol:,}</div>
    <div class="vol-sub">{fmt_vol(p_vol)} shares &nbsp;·&nbsp; {vol_vs}</div>
    {vol_bar_html(p_buy, p_sell)}
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  HISTORICAL OVERVIEW
# ─────────────────────────────────────────────────────
ath      = float(hist["High"].max())
ath_date = hist["High"].idxmax().strftime("%d %b %Y")
atl      = float(hist["Low"].min())
atl_date = hist["Low"].idxmin().strftime("%d %b %Y")
l_date   = hist.index[0].strftime("%d %b %Y")
l_price  = float(hist["Close"].iloc[0])
l_vol    = int(hist["Volume"].iloc[0])

st.markdown('<div class="section-label">Historical Overview — Since Listing</div>', unsafe_allow_html=True)
h1, h2, h3, h4 = st.columns(4)
for col, extra, lbl, val, sub in [
    (h1, "",              "📅 Listing Date",  l_date,           "First day on NSE"),
    (h2, "",              "💰 Listing Price", fmt_price(l_price), f"Vol: {fmt_vol(l_vol)}"),
    (h3, "hist-card-high","🏆 All-Time High", fmt_price(ath),   ath_date),
    (h4, "hist-card-low", "📉 All-Time Low",  fmt_price(atl),   atl_date),
]:
    with col:
        st.markdown(f'<div class="hist-card {extra}"><div class="hist-card-lbl">{lbl}</div><div class="hist-card-val">{val}</div><div class="hist-card-sub">{sub}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  PRICE HISTORY — with frequency selector
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Price History</div>', unsafe_allow_html=True)

freq = st.radio(
    "", list(TIMEFRAMES.keys()),
    index=3, horizontal=True,
    label_visibility="collapsed",
    key="price_freq",
)
hist_view = load_period(ticker, TIMEFRAMES[freq])

fig_p = go.Figure(go.Scatter(
    x=hist_view.index, y=hist_view["Close"], mode="lines",
    line=dict(color="#38bdf8", width=1.8),
    fill="tozeroy", fillcolor="rgba(56,189,248,0.05)",
    hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.2f}<extra></extra>",
))
fig_p.update_layout(**PLOT_BASE, height=330)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  VOLUME HISTORY — green/red by day direction
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Volume History</div>', unsafe_allow_html=True)

bar_colors = [
    "rgba(16,185,129,0.65)" if c >= o else "rgba(239,68,68,0.65)"
    for c, o in zip(hist_view["Close"], hist_view["Open"])
]

fig_v = go.Figure(go.Bar(
    x=hist_view.index,
    y=hist_view["Volume"],
    marker=dict(color=bar_colors, line=dict(width=0)),
    hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,} shares<extra></extra>",
))
vol_layout = {**PLOT_BASE, "yaxis": {**PLOT_BASE["yaxis"], "tickprefix": ""}}
fig_v.update_layout(**vol_layout, height=250)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; gap:1.5rem; padding:.5rem .3rem 0;">
    <span style="color:#6ee7b7; font-size:.75rem; font-weight:600;">🟢 Up Day — Buying Pressure</span>
    <span style="color:#fca5a5; font-size:.75rem; font-weight:600;">🔴 Down Day — Selling Pressure</span>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-footer">
    Data via Yahoo Finance &nbsp;·&nbsp; Live price refreshes every 3s &nbsp;·&nbsp;
    Buy/Sell split estimated from price-position within bar &nbsp;·&nbsp; For analysis only, not financial advice<br>
    Page loaded: {datetime.now().strftime('%d %b %Y, %H:%M:%S')} IST
</div>
""", unsafe_allow_html=True)
