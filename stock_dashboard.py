"""
╔══════════════════════════════════════════════════════╗
║      NSE STOCK DASHBOARD v3 — Full Analytics Suite  ║
║      Bob (Analyst) + Rob (Dev)  |  2026              ║
╚══════════════════════════════════════════════════════╝
Run:   streamlit run stock_dashboard.py
Deps:  pip install -r requirements.txt
WATCHLIST: edit the dict below to add/remove any stock.
"""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
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
#  CSS
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
*,html,body,[class*="css"]{font-family:'DM Sans',sans-serif !important;}
.stApp{background:#070b14;}
.block-container{padding:2rem 2.5rem 4rem !important;max-width:1440px;}

/* Header */
.dash-header{text-align:center;padding:2rem 0 1rem;margin-bottom:1.5rem;}
.dash-title{font-size:2.4rem;font-weight:700;letter-spacing:-1px;color:#f1f5f9;margin-bottom:.3rem;}
.dash-title span{background:linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.dash-sub{color:#334155;font-size:.85rem;letter-spacing:2.5px;text-transform:uppercase;font-weight:500;}

/* Segmented control */
div[data-testid="stSegmentedControl"]>div{background:#0d1424 !important;border:1px solid #1e293b !important;border-radius:50px !important;padding:4px !important;gap:4px !important;}
div[data-testid="stSegmentedControl"] button{border-radius:50px !important;font-weight:600 !important;font-size:.92rem !important;color:#475569 !important;padding:.45rem 1.4rem !important;transition:all .2s !important;border:none !important;}
div[data-testid="stSegmentedControl"] button[aria-checked="true"]{background:linear-gradient(135deg,#1d4ed8,#7c3aed) !important;color:#fff !important;box-shadow:0 2px 12px rgba(99,102,241,.35) !important;}
div[data-testid="stSegmentedControl"] label{display:none !important;}

/* Radio as pills */
div[data-testid="stRadio"]>div{flex-direction:row !important;gap:6px !important;flex-wrap:wrap !important;}
div[data-testid="stRadio"] label{background:#0f172a;border:1px solid #1e293b;border-radius:50px;padding:.3rem 1rem;cursor:pointer;transition:all .2s;color:#475569;font-weight:600;font-size:.82rem;}
div[data-testid="stRadio"] label:has(input:checked){background:linear-gradient(135deg,#0ea5e9,#6366f1);border-color:transparent;color:#fff;box-shadow:0 2px 10px rgba(56,189,248,.25);}
div[data-testid="stRadio"] input[type=radio]{display:none;}
div[data-testid="stRadio"]>label{display:none !important;}

/* Section labels with accent per type */
.section-label{font-size:.68rem;letter-spacing:2.5px;text-transform:uppercase;color:#334155;font-weight:700;margin:1.8rem 0 .9rem;border-left:3px solid #38bdf8;padding-left:10px;}
.section-label.val  {border-left-color:#818cf8;}
.section-label.health{border-left-color:#10b981;}
.section-label.growth{border-left-color:#f59e0b;}
.section-label.owner{border-left-color:#06b6d4;}
.section-label.analyst{border-left-color:#fbbf24;}
.section-label.news_{border-left-color:#64748b;}
.section-label.hist {border-left-color:#c084fc;}

/* Live price hero */
.price-hero{background:linear-gradient(135deg,#0f172a 0%,#111827 60%,#0f172a 100%);border:1px solid #1e293b;border-radius:20px;padding:2rem 2.5rem;box-shadow:0 8px 40px rgba(56,189,248,.06);display:flex;align-items:center;justify-content:space-between;margin-bottom:1.4rem;position:relative;overflow:hidden;}
.price-hero::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,rgba(56,189,248,.06) 0%,transparent 70%);border-radius:50%;}
.price-tag{font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#475569;font-weight:600;margin-bottom:.5rem;}
.price-value{font-size:3rem;font-weight:700;color:#f1f5f9;letter-spacing:-1.5px;line-height:1;font-family:'DM Mono',monospace !important;}
.price-change-pos{display:inline-block;margin-top:.6rem;background:rgba(16,185,129,.12);color:#10b981;border:1px solid rgba(16,185,129,.25);border-radius:8px;padding:.2rem .65rem;font-size:.92rem;font-weight:600;font-family:'DM Mono',monospace !important;}
.price-change-neg{display:inline-block;margin-top:.6rem;background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.25);border-radius:8px;padding:.2rem .65rem;font-size:.92rem;font-weight:600;font-family:'DM Mono',monospace !important;}
.prev-close-lbl{font-size:.7rem;letter-spacing:1.5px;text-transform:uppercase;color:#334155;font-weight:600;margin-bottom:.3rem;text-align:right;}
.prev-close-val{font-size:1.25rem;color:#64748b;font-weight:600;font-family:'DM Mono',monospace !important;text-align:right;}

/* OHLC stat cards */
.stat-card{border-radius:16px;padding:1.3rem 1.4rem;height:105px;display:flex;flex-direction:column;justify-content:space-between;}
.stat-card-lbl{font-size:.66rem;letter-spacing:2px;text-transform:uppercase;font-weight:700;opacity:.6;}
.stat-card-val{font-size:1.5rem;font-weight:700;letter-spacing:-.5px;font-family:'DM Mono',monospace !important;line-height:1;}
.card-high {background:linear-gradient(135deg,#052e16,#064e3b);border:1px solid rgba(16,185,129,.2);box-shadow:0 4px 20px rgba(16,185,129,.08);color:#6ee7b7;}
.card-low  {background:linear-gradient(135deg,#1c0505,#450a0a);border:1px solid rgba(239,68,68,.2);box-shadow:0 4px 20px rgba(239,68,68,.08);color:#fca5a5;}
.card-open {background:linear-gradient(135deg,#0d1323,#1e1b4b);border:1px solid rgba(129,140,248,.2);box-shadow:0 4px 20px rgba(129,140,248,.08);color:#a5b4fc;}
.card-close{background:linear-gradient(135deg,#111827,#1f2937);border:1px solid rgba(148,163,184,.15);box-shadow:0 4px 20px rgba(148,163,184,.05);color:#94a3b8;}

/* Volume card */
.volume-card{background:linear-gradient(135deg,#0a1628,#0c1e3a);border:1px solid rgba(56,189,248,.18);border-radius:16px;padding:1.3rem 1.8rem;box-shadow:0 4px 24px rgba(56,189,248,.07);margin:.8rem 0;}
.vol-title{font-size:.68rem;letter-spacing:2px;text-transform:uppercase;color:#38bdf8;font-weight:700;opacity:.7;margin-bottom:.4rem;}
.vol-total{font-size:1.8rem;font-weight:700;color:#38bdf8;font-family:'DM Mono',monospace !important;letter-spacing:-.5px;}
.vol-sub{font-size:.78rem;color:#334155;margin-top:.2rem;}

/* Generic metric card */
.m-card{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:1.1rem 1.3rem;box-shadow:0 4px 16px rgba(0,0,0,.3);height:100px;display:flex;flex-direction:column;justify-content:space-between;}
.m-card-lbl{font-size:.63rem;letter-spacing:1.8px;text-transform:uppercase;color:#334155;font-weight:700;}
.m-card-val{font-size:1.3rem;font-weight:700;color:#e2e8f0;font-family:'DM Mono',monospace !important;letter-spacing:-.3px;}
.m-card-sub{font-size:.65rem;color:#475569;}
.m-good{border-color:rgba(16,185,129,.25);box-shadow:0 4px 16px rgba(16,185,129,.08);}
.m-good .m-card-val{color:#10b981;}
.m-warn{border-color:rgba(251,191,36,.25);box-shadow:0 4px 16px rgba(251,191,36,.08);}
.m-warn .m-card-val{color:#fbbf24;}
.m-bad {border-color:rgba(239,68,68,.25);box-shadow:0 4px 16px rgba(239,68,68,.08);}
.m-bad  .m-card-val{color:#ef4444;}

/* Historical cards */
.hist-card{background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:1.3rem 1.4rem;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,.3);}
.hist-card-lbl{font-size:.63rem;letter-spacing:2px;text-transform:uppercase;color:#334155;font-weight:700;margin-bottom:.5rem;}
.hist-card-val{font-size:1.1rem;font-weight:700;color:#e2e8f0;font-family:'DM Mono',monospace !important;}
.hist-card-sub{font-size:.7rem;color:#475569;margin-top:.3rem;}
.hist-card-high .hist-card-val{color:#10b981;}
.hist-card-low  .hist-card-val{color:#ef4444;}

/* Analyst card */
.analyst-hero{background:linear-gradient(135deg,#0d1a0d,#111f11);border:1px solid rgba(251,191,36,.2);border-radius:18px;padding:1.6rem 2rem;box-shadow:0 6px 28px rgba(251,191,36,.06);display:flex;align-items:center;justify-content:space-between;margin:.8rem 0;}
.analyst-target{font-size:.68rem;letter-spacing:2px;text-transform:uppercase;color:#64748b;font-weight:700;margin-bottom:.4rem;}
.analyst-price{font-size:2.4rem;font-weight:700;color:#fbbf24;font-family:'DM Mono',monospace !important;letter-spacing:-1px;}
.rec-badge{display:inline-block;border-radius:50px;padding:.4rem 1.2rem;font-size:.9rem;font-weight:700;letter-spacing:.5px;}

/* News */
.news-item{background:#0d1117;border:1px solid #1e293b;border-radius:12px;padding:1rem 1.2rem;margin-bottom:.6rem;transition:border-color .2s;cursor:pointer;}
.news-item:hover{border-color:#334155;}
.news-title{color:#e2e8f0;font-size:.88rem;font-weight:600;line-height:1.4;margin-bottom:.35rem;}
.news-meta{color:#334155;font-size:.7rem;font-weight:500;}

/* Chart wrapper */
.chart-wrap{background:#0a0f1e;border:1px solid #1e293b;border-radius:18px;padding:1rem;margin-top:.4rem;box-shadow:0 4px 30px rgba(0,0,0,.4);}

/* Footer */
.dash-footer{text-align:center;padding:2rem 0 1rem;color:#1e293b;font-size:.72rem;letter-spacing:.5px;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  WATCHLIST — edit freely
# ─────────────────────────────────────────────────────
WATCHLIST = {
    # ── Top 20 Nifty 50 by Index Weightage (May 2026) ──────────────
    "🛢️  Reliance Industries": "RELIANCE.NS",
    "🏦 HDFC Bank":            "HDFCBANK.NS",
    "📡 Bharti Airtel":        "BHARTIARTL.NS",
    "🏦 ICICI Bank":           "ICICIBANK.NS",
    "🏦 SBI":                  "SBIN.NS",
    "💻 TCS":                  "TCS.NS",
    "💳 Bajaj Finance":        "BAJFINANCE.NS",
    "🏗️  L&T":                 "LT.NS",
    "🛒 Hindustan Unilever":   "HINDUNILVR.NS",
    "💻 Infosys":              "INFY.NS",
    "💊 Sun Pharma":           "SUNPHARMA.NS",
    "🚢 Adani Ports":          "ADANIPORTS.NS",
    "🚗 Maruti Suzuki":        "MARUTI.NS",
    "🏦 Kotak Mahindra Bank":  "KOTAKBANK.NS",
    "🚬 ITC":                  "ITC.NS",
    "🚗 Tata Motors":          "TATAMOTORS.NS",
    "💻 HCL Technologies":     "HCLTECH.NS",
    "🏦 Axis Bank":            "AXISBANK.NS",
    "⚡ Power Grid Corp":      "POWERGRID.NS",
    "💎 Titan Company":        "TITAN.NS",
    # ── Add more below ↓ ───────────────────────────────────────────
}

TIMEFRAMES = {
    "1M":"1mo","3M":"3mo","6M":"6mo",
    "1Y":"1y","3Y":"3y","5Y":"5y","All":"max",
}

PLOT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,15,30,0.6)",
    font=dict(family="DM Sans", color="#475569", size=12),
    margin=dict(l=12,r=12,t=16,b=12),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)",showgrid=True,zeroline=False,rangeslider=dict(visible=False)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)",showgrid=True,zeroline=False,tickprefix="₹"),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#0f172a",bordercolor="#1e293b",font=dict(color="#e2e8f0",size=12)),
    showlegend=False,
)

# ─────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────
def fmt_price(v):  return f"₹{v:,.2f}" if v else "N/A"
def fmt_pct(v):    return f"{v*100:.2f}%" if v else "N/A"
def fmt_cr(v):     return f"₹{v/1e7:.2f} Cr" if v and abs(v)>=1e7 else (f"₹{v/1e5:.1f} L" if v and abs(v)>=1e5 else (f"₹{v:,.0f}" if v else "N/A"))
def fmt_x(v):      return f"{v:.2f}x" if v and v>0 else "N/A"
def fmt_eps(v):    return f"₹{v:.2f}" if v else "N/A"
def fmt_vol(v):
    if v>=1e7:    return f"{v/1e7:.2f} Cr"
    elif v>=1e5:  return f"{v/1e5:.2f} L"
    elif v>=1e3:  return f"{v/1e3:.1f} K"
    return f"{v:,.0f}"

def safe(d, *keys, default=None):
    for k in keys:
        v = d.get(k)
        if v is not None: return v
    return default

def health_cls(val, good, warn):
    """Return CSS class based on thresholds. good/warn are upper bounds."""
    if val is None: return ""
    if val <= good:  return "m-good"
    if val <= warn:  return "m-warn"
    return "m-bad"

def health_cls_inv(val, bad, warn):
    """Inverse: higher is better."""
    if val is None: return ""
    if val >= warn:  return "m-good"
    if val >= bad:   return "m-warn"
    return "m-bad"

def calculate_rsi(prices, period=14):
    delta = prices.diff().dropna()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    ag    = gain.ewm(com=period-1, min_periods=period).mean()
    al    = loss.ewm(com=period-1, min_periods=period).mean()
    rs    = ag / al
    return round(float((100 - 100/(1+rs)).iloc[-1]), 2)

def rsi_meta(rsi):
    if rsi < 30:   return "Oversold", "#10b981", "Potential bounce zone"
    if rsi < 45:   return "Bearish",  "#f59e0b", "Below midline, weak"
    if rsi < 55:   return "Neutral",  "#94a3b8", "No clear signal"
    if rsi < 70:   return "Bullish",  "#38bdf8", "Momentum building"
    return          "Overbought","#ef4444", "May pull back soon"

def buy_sell_estimate(row):
    h,l,c,v = float(row["High"]),float(row["Low"]),float(row["Close"]),int(row["Volume"])
    bp = ((c-l)/(h-l)) if (h-l)>0 else 0.5
    return int(v*bp), int(v*(1-bp))

def vol_bar_html(buy_vol, sell_vol):
    total = buy_vol+sell_vol or 1
    bp    = int(buy_vol/total*100)
    sp    = 100-bp
    return (
        f'<div style="margin-top:.8rem">'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:5px">'
        f'<span style="color:#10b981;font-size:.78rem;font-weight:600">🟢 Buy {bp}%  {fmt_vol(buy_vol)}</span>'
        f'<span style="color:#ef4444;font-size:.78rem;font-weight:600">{fmt_vol(sell_vol)}  {sp}% Sell 🔴</span>'
        f'</div>'
        f'<div style="background:#1e293b;border-radius:6px;height:8px;overflow:hidden">'
        f'<div style="background:linear-gradient(90deg,#10b981,#34d399);width:{bp}%;height:100%"></div>'
        f'</div></div>'
    )

def generate_analyst_reasons(info):
    """Auto-generate analyst reasoning bullets from available stock metrics."""
    reasons = []
    target   = info.get("targetMeanPrice")
    curr     = info.get("currentPrice") or info.get("regularMarketPrice")
    pe       = info.get("trailingPE")
    roe      = info.get("returnOnEquity")
    de       = info.get("debtToEquity")
    rev_g    = info.get("revenueGrowth")
    margins  = info.get("profitMargins")

    if target and curr:
        up = (target - curr) / curr * 100
        if up > 20:   reasons.append(("🚀","Strong re-rating potential",     f"Consensus implies {up:.1f}% upside — analysts see clear undervaluation vs intrinsic value"))
        elif up > 5:  reasons.append(("📈","Moderate upside priced in",       f"Target implies {up:.1f}% upside — steady appreciation expected, no major catalyst needed"))
        elif up > -5: reasons.append(("⚖️","Stock near fair value",            f"Target within {abs(up):.1f}% of price — analysts see limited upside/downside from here"))
        else:         reasons.append(("⚠️","Stock above consensus target",     f"Price is {abs(up):.1f}% above mean target — analysts flagging overvaluation risk"))

    if pe:
        if pe < 12:   reasons.append(("💰","Deep value P/E",                  f"P/E of {pe:.1f}x is well below market average — earnings are cheap relative to price"))
        elif pe < 20: reasons.append(("✅","Reasonable earnings multiple",     f"P/E of {pe:.1f}x in fair-value zone — not expensive vs peers or history"))
        elif pe < 35: reasons.append(("📊","Growth premium baked in",         f"P/E of {pe:.1f}x reflects expectation of strong future earnings growth"))
        else:         reasons.append(("⚠️","High P/E demands growth delivery", f"P/E of {pe:.1f}x — target assumes sustained high EPS growth to justify valuation"))

    if roe:
        r = roe * 100
        if r > 20:    reasons.append(("💪","Exceptional capital efficiency",   f"ROE of {r:.1f}% — management generating strong shareholder returns, justifies premium"))
        elif r > 12:  reasons.append(("👍","Solid return on equity",           f"ROE {r:.1f}% above cost of equity — consistent value creation supports the target"))
        else:         reasons.append(("📉","Weak ROE caps the multiple",        f"ROE {r:.1f}% below hurdle rate — limits how high analysts can justify the valuation"))

    if rev_g:
        rg = rev_g * 100
        if rg > 20:   reasons.append(("🚀","High revenue growth momentum",    f"Revenue up {rg:.1f}% YoY — strong topline gives analysts confidence in target"))
        elif rg > 8:  reasons.append(("📈","Healthy topline growth",           f"Revenue growing {rg:.1f}% YoY — steady growth baked into the target price"))
        elif rg < 0:  reasons.append(("⚠️","Revenue contraction is a risk",    f"Revenue declined {abs(rg):.1f}% — analysts cautious, reflected in conservative target"))

    if de:
        dr = de / 100
        if dr > 3:    reasons.append(("⚖️","High leverage is key risk",        f"D/E of {dr:.1f}x — heavy debt burden is primary risk analysts discount in their target"))
        elif dr < 0.3:reasons.append(("💚","Clean balance sheet premium",       f"D/E of {dr:.1f}x — near debt-free; financial strength supports a higher valuation multiple"))

    if margins:
        m = margins * 100
        if m > 20:    reasons.append(("💎","Strong pricing power",             f"Net margin {m:.1f}% — high margin business with strong moat, supports premium target"))
        elif m < 5:   reasons.append(("📉","Thin margins limit earnings lever", f"Net margin {m:.1f}% — low-margin business; small revenue miss hits profits hard"))

    if not reasons:
        reasons.append(("ℹ️","Insufficient data", "Analyst reasoning could not be auto-generated — check screener.in or NSE for broker reports"))
    return reasons[:5]


def mc(cls,lbl,val,sub=""):
    return (
        f'<div class="m-card {cls}">'
        f'<div class="m-card-lbl">{lbl}</div>'
        f'<div class="m-card-val">{val}</div>'
        f'<div class="m-card-sub">{sub}</div>'
        f'</div>'
    )

# ─────────────────────────────────────────────────────
#  CACHE FUNCTIONS
# ─────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_full_history(ticker):
    tk   = yf.Ticker(ticker)
    info = tk.info
    hist = tk.history(period="max", auto_adjust=True)
    hist.index = hist.index.tz_localize(None)
    return info, hist

@st.cache_data(ttl=300)
def load_period(ticker, period):
    h = yf.Ticker(ticker).history(period=period, auto_adjust=True)
    h.index = h.index.tz_localize(None)
    return h

@st.cache_data(ttl=3600)
def load_fundamentals(ticker):
    tk = yf.Ticker(ticker)
    def safe_df(fn):
        try:
            df = fn()
            if df is not None and not df.empty:
                df.columns = pd.to_datetime(df.columns).tz_localize(None)
                return df
        except: pass
        return pd.DataFrame()

    fin  = safe_df(lambda: tk.income_stmt)
    cf   = safe_df(lambda: tk.cashflow)
    news = []
    try: news = tk.news[:8]
    except: pass
    holders = None
    try: holders = tk.major_holders
    except: pass
    upgrades = pd.DataFrame()
    try:
        ud = tk.upgrades_downgrades
        if ud is not None and not ud.empty:
            ud = ud.copy()
            if ud.index.tz is not None:
                ud.index = ud.index.tz_localize(None)
            upgrades = ud.head(12).reset_index()
    except: pass
    return fin, cf, news, holders, upgrades

@st.cache_data(ttl=3600)
def get_pe_history(ticker):
    tk = yf.Ticker(ticker)
    info = tk.info
    trailing_pe  = info.get("trailingPE")
    forward_pe   = info.get("forwardPE")
    trailing_eps = info.get("trailingEps")
    try:
        q = tk.quarterly_income_stmt
        h = tk.history(period="max", auto_adjust=True)
        h.index = h.index.tz_localize(None)
        shares = info.get("sharesOutstanding") or info.get("floatShares") or 0
        if not q.empty and shares>0 and "Net Income" in q.index:
            ni = q.loc["Net Income"].dropna().sort_index()
            ni.index = pd.DatetimeIndex(ni.index).tz_localize(None)
            ttm = ni.rolling(4).sum() / shares
            rows = []
            for dt,price in zip(h.index, h["Close"]):
                av = ttm[ttm.index<=dt].dropna()
                if not av.empty:
                    e = float(av.iloc[-1])
                    if e>0: rows.append((dt,round(price/e,2)))
            if len(rows)>10:
                d,v = zip(*rows)
                return trailing_pe,forward_pe,trailing_eps,pd.Series(v,index=pd.DatetimeIndex(d))
    except: pass
    if trailing_eps and trailing_eps>0:
        h = yf.Ticker(ticker).history(period="max",auto_adjust=True)
        h.index = h.index.tz_localize(None)
        return trailing_pe,forward_pe,trailing_eps,(h["Close"]/trailing_eps).round(2)
    return trailing_pe,forward_pe,trailing_eps,None

# ─────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────
st.markdown("""<div class="dash-header"><div class="dash-title">📊 <span>Stock</span> Dashboard</div><div class="dash-sub">NSE Live Tracker &nbsp;·&nbsp; Full Analytics Suite</div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  STOCK SELECTOR
# ─────────────────────────────────────────────────────
_,mid,_ = st.columns([1,3,1])
with mid:
    chosen = st.segmented_control("s",list(WATCHLIST.keys()),default=list(WATCHLIST.keys())[0],label_visibility="hidden",key="stock_seg")
if not chosen: chosen=list(WATCHLIST.keys())[0]
ticker = WATCHLIST[chosen]

# ─────────────────────────────────────────────────────
#  LOAD ALL DATA
# ─────────────────────────────────────────────────────
with st.spinner("Loading market data..."):
    info, hist = load_full_history(ticker)
    fin, cf, news_items, holders, upgrades_df = load_fundamentals(ticker)
    trailing_pe, forward_pe, trailing_eps, pe_series = get_pe_history(ticker)

if hist.empty:
    st.error("Could not load data."); st.stop()

st.session_state["_ticker"]     = ticker
st.session_state["_prev_close"] = info.get("previousClose") or float(hist["Close"].iloc[-2])

# ─────────────────────────────────────────────────────
#  LIVE PRICE — refreshes every 3s
# ─────────────────────────────────────────────────────
@st.fragment(run_every=3)
def live_price_card():
    _tk = st.session_state.get("_ticker","")
    _pc = st.session_state.get("_prev_close",0)
    try:
        fresh = yf.Ticker(_tk).info
        curr  = fresh.get("currentPrice") or fresh.get("regularMarketPrice") or float(hist["Close"].iloc[-1])
    except:
        curr = float(hist["Close"].iloc[-1])
    chg=curr-_pc; pct=(chg/_pc*100) if _pc else 0
    badge="price-change-pos" if chg>=0 else "price-change-neg"
    arrow="▲" if chg>=0 else "▼"
    ts=datetime.now().strftime("%H:%M:%S")
    st.markdown(f'''<div class="price-hero"><div><div class="price-tag">Live Price · NSE · <span style="color:#1e3a5f;font-family:DM Mono,monospace">{ts}</span></div><div class="price-value">{fmt_price(curr)}</div><span class="{badge}">{arrow} {fmt_price(abs(chg))} ({pct:+.2f}%)</span></div><div><div class="prev-close-lbl">Previous Close</div><div class="prev-close-val">{fmt_price(_pc)}</div></div></div>''', unsafe_allow_html=True)

live_price_card()

# ─────────────────────────────────────────────────────
#  TODAY
# ─────────────────────────────────────────────────────
today   = hist.iloc[-1]
tb,ts_v = buy_sell_estimate(today)
tv      = int(today["Volume"])
st.markdown('<div class="section-label">Today — Current Session</div>', unsafe_allow_html=True)
c1,c2,c3,c4=st.columns(4)
for col,cls,lbl,val in[(c1,"card-high","🔼 Day High",fmt_price(float(today["High"]))),(c2,"card-low","🔽 Day Low",fmt_price(float(today["Low"]))),(c3,"card-open","○ Day Open",fmt_price(float(today["Open"]))),(c4,"card-close","● Day Close",fmt_price(float(today["Close"])))]:
    with col: st.markdown(f'<div class="stat-card {cls}"><div class="stat-card-lbl">{lbl}</div><div class="stat-card-val">{val}</div></div>',unsafe_allow_html=True)
st.markdown(f'''<div class="volume-card"><div class="vol-title">📦 Today Volume</div><div class="vol-total">{tv:,}</div><div class="vol-sub">{fmt_vol(tv)} shares</div>{vol_bar_html(tb,ts_v)}</div>''',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  PREVIOUS DAY
# ─────────────────────────────────────────────────────
prev=hist.iloc[-2]; pb,ps_v=buy_sell_estimate(prev); pv=int(prev["Volume"])
avg_v=int(hist["Volume"].mean()); vr=pv/avg_v if avg_v else 1
vl=f"{{'↑' if vr>=1 else '↓'}} {abs(vr-1)*100:.0f}% vs avg daily"
st.markdown('<div class="section-label">Previous Day — OHLC</div>',unsafe_allow_html=True)
p1,p2,p3,p4=st.columns(4)
for col,cls,lbl,val in[(p1,"card-high","🔼 Prev High",fmt_price(float(prev["High"]))),(p2,"card-low","🔽 Prev Low",fmt_price(float(prev["Low"]))),(p3,"card-open","○ Prev Open",fmt_price(float(prev["Open"]))),(p4,"card-close","● Prev Close",fmt_price(float(prev["Close"])))]:
    with col: st.markdown(f'<div class="stat-card {cls}"><div class="stat-card-lbl">{lbl}</div><div class="stat-card-val">{val}</div></div>',unsafe_allow_html=True)
st.markdown(f'''<div class="volume-card"><div class="vol-title">📦 Previous Day Volume</div><div class="vol-total">{pv:,}</div><div class="vol-sub">{fmt_vol(pv)} shares · {vl}</div>{vol_bar_html(pb,ps_v)}</div>''',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  VOLUME — PERIOD AVERAGES
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Volume — Period Averages</div>', unsafe_allow_html=True)

def avg_vol_for(n_days):
    return int(hist["Volume"].tail(n_days).mean()) if len(hist) >= n_days else None

v5d  = avg_vol_for(5)
v20d = avg_vol_for(20)
v50d = avg_vol_for(50)
v1y  = avg_vol_for(252)

today_vol_now = int(today["Volume"])

def vol_vs(base, compare):
    if not base or not compare: return ""
    diff = (compare - base) / base * 100
    arrow = "↑" if diff >= 0 else "↓"
    col   = "#10b981" if diff >= 0 else "#ef4444"
    return f'<span style="color:{col};font-size:.7rem;font-weight:600">{arrow} {abs(diff):.0f}%</span>'

va1,va2,va3,va4 = st.columns(4)
for col, lbl, val, compare_val in [
    (va1, "📊 5-Day Avg",   v5d,  today_vol_now),
    (va2, "📊 20-Day Avg",  v20d, today_vol_now),
    (va3, "📊 50-Day Avg",  v50d, today_vol_now),
    (va4, "📊 1-Year Avg",  v1y,  today_vol_now),
]:
    diff_html = vol_vs(val, compare_val) if val else ""
    with col:
        st.markdown(
            f'<div class="m-card"><div class="m-card-lbl">{lbl}</div>'
            f'<div class="m-card-val" style="font-size:1.1rem">{fmt_vol(val) if val else "N/A"}</div>'
            f'<div class="m-card-sub">Today vs this avg: {diff_html}</div></div>',
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────────────
#  TECHNICAL SIGNALS
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Technical Signals</div>',unsafe_allow_html=True)

rsi_val  = calculate_rsi(hist["Close"])
rsi_lbl, rsi_col, rsi_hint = rsi_meta(rsi_val)
w52h     = safe(info,"fiftyTwoWeekHigh")
w52l     = safe(info,"fiftyTwoWeekLow")
dma200   = safe(info,"twoHundredDayAverage")
dma50    = safe(info,"fiftyDayAverage")
beta_v   = safe(info,"beta")
curr_p   = safe(info,"currentPrice","regularMarketPrice") or float(hist["Close"].iloc[-1])

pct_52h  = ((curr_p-w52h)/w52h*100) if w52h else None
pct_52l  = ((curr_p-w52l)/w52l*100) if w52l else None
pct_200  = ((curr_p-dma200)/dma200*100) if dma200 else None
pct_50   = ((curr_p-dma50)/dma50*100) if dma50 else None

# RSI gauge
fig_rsi = go.Figure(go.Indicator(
    mode="gauge+number",
    value=rsi_val,
    number={"font":{"size":32,"color":rsi_col,"family":"DM Mono"}},
    gauge={
        "axis":{"range":[0,100],"tickcolor":"#1e293b","tickfont":{"color":"#334155","size":10}},
        "bar":{"color":rsi_col,"thickness":0.25},
        "bgcolor":"rgba(0,0,0,0)",
        "borderwidth":0,
        "steps":[
            {"range":[0,30],"color":"rgba(16,185,129,0.12)"},
            {"range":[30,70],"color":"rgba(148,163,184,0.05)"},
            {"range":[70,100],"color":"rgba(239,68,68,0.12)"},
        ],
        "threshold":{"line":{"color":rsi_col,"width":3},"thickness":0.75,"value":rsi_val},
    },
))
fig_rsi.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    height=180,margin=dict(l=20,r=20,t=30,b=10),font=dict(family="DM Sans",color="#475569"))

t_col, r_col = st.columns([1.2,2])
with t_col:
    st.markdown('<div class="chart-wrap" style="padding:.5rem">',unsafe_allow_html=True)
    st.plotly_chart(fig_rsi,use_container_width=True,config={"displayModeBar":False})
    st.markdown(f'''<div style="text-align:center;margin-top:-.5rem;padding-bottom:.5rem"><span style="color:{rsi_col};font-size:.95rem;font-weight:700">{rsi_lbl}</span><div style="color:#475569;font-size:.72rem;margin-top:.2rem">{rsi_hint}</div></div>''',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

with r_col:
    r1,r2,r3,r4=st.columns(4)
    dma200_cls = "m-good" if pct_200 and pct_200>0 else ("m-bad" if pct_200 and pct_200<-10 else "m-warn")
    dma50_cls  = "m-good" if pct_50  and pct_50>0  else ("m-bad" if pct_50  and pct_50<-10  else "m-warn")
    for col,cls,lbl,val,sub in[
        (r1,"m-warn","📅 52W High",fmt_price(w52h),f"{pct_52h:+.1f}% from high" if pct_52h else ""),
        (r2,"m-good","📅 52W Low", fmt_price(w52l), f"{pct_52l:+.1f}% from low"  if pct_52l else ""),
        (r3,dma200_cls,"〰 vs 200 DMA",fmt_price(dma200),f"{pct_200:+.1f}% {'above ✅' if pct_200 and pct_200>0 else 'below ⚠️'}" if pct_200 else ""),
        (r4,dma50_cls, "〰 vs 50 DMA", fmt_price(dma50), f"{pct_50:+.1f}%  {'above ✅' if pct_50  and pct_50>0  else 'below ⚠️'}" if pct_50  else ""),
    ]:
        with col: st.markdown(mc(cls,lbl,val,sub),unsafe_allow_html=True)

    b_cls = "m-warn" if beta_v and 1<=beta_v<=1.5 else ("m-bad" if beta_v and beta_v>1.5 else "m-good")
    mkt_cap = safe(info,"marketCap")
    st.markdown("<div style='height:.6rem'></div>",unsafe_allow_html=True)
    b1,b2=st.columns(2)
    with b1: st.markdown(mc(b_cls,"⚡ Beta",f"{beta_v:.2f}" if beta_v else "N/A","<1 stable · >1 volatile"),unsafe_allow_html=True)
    with b2: st.markdown(mc("","🏦 Market Cap",fmt_cr(mkt_cap),"Total market value"),unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  VALUATION
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label val">Valuation Metrics</div>',unsafe_allow_html=True)

pb_v   = safe(info,"priceToBook")
ev_eb  = safe(info,"enterpriseToEbitda")
ps_v   = safe(info,"priceToSalesTrailing12Months")
div_y  = safe(info,"dividendYield")
payout = safe(info,"payoutRatio")
fwd_pe = safe(info,"forwardPE")
tr_pe  = safe(info,"trailingPE")

def pe_cls(v):
    if not v: return ""
    return "m-good" if v<15 else ("m-warn" if v<25 else "m-bad")

v1,v2,v3,v4=st.columns(4)
for col,cls,lbl,val,sub in[
    (v1,pe_cls(tr_pe),"📊 Trailing P/E",fmt_x(tr_pe),"< 15 cheap · > 25 expensive"),
    (v2,pe_cls(fwd_pe),"🔭 Forward P/E",fmt_x(fwd_pe),"Based on est. earnings"),
    (v3,"","📖 Price/Book",fmt_x(pb_v),"< 1 undervalued vs assets"),
    (v4,"","🏭 EV/EBITDA",fmt_x(ev_eb),"< 10 attractive"),
]:
    with col: st.markdown(mc(cls,lbl,val,sub),unsafe_allow_html=True)

st.markdown("<div style='height:.4rem'></div>",unsafe_allow_html=True)
v5,v6,v7,v8=st.columns(4)
for col,cls,lbl,val,sub in[
    (v5,"","💵 Trailing EPS",fmt_eps(trailing_eps),"Earnings per share TTM"),
    (v6,"","💹 Price/Sales",fmt_x(ps_v),"Revenue multiple"),
    (v7,"m-good" if div_y and div_y>0.02 else "","💰 Div Yield",fmt_pct(div_y),"Annual dividend / price"),
    (v8,"","🔄 Payout Ratio",fmt_pct(payout),"% of earnings paid as div"),
]:
    with col: st.markdown(mc(cls,lbl,val,sub),unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  FINANCIAL HEALTH
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label health">Financial Health</div>',unsafe_allow_html=True)

de_v   = safe(info,"debtToEquity")
cr_v   = safe(info,"currentRatio")
roe_v  = safe(info,"returnOnEquity")
roa_v  = safe(info,"returnOnAssets")
om_v   = safe(info,"operatingMargins")
nm_v   = safe(info,"profitMargins")
fcf_v  = safe(info,"freeCashflow")
ebitda_v = safe(info,"ebitda")

# Interest coverage from financials
int_cov = None
try:
    if not fin.empty:
        ops = None; int_exp = None
        for key in ["Operating Income","EBIT","Pretax Income"]:
            if key in fin.index: ops=float(fin.loc[key].iloc[0]); break
        for key in ["Interest Expense","Net Interest Income"]:
            if key in fin.index: int_exp=abs(float(fin.loc[key].iloc[0])); break
        if ops and int_exp and int_exp!=0: int_cov=round(ops/int_exp,2)
except: pass

de_cls  = health_cls(de_v/100 if de_v else None, 1, 2) if de_v else ""
cr_cls  = health_cls_inv(cr_v, 1.0, 1.5)
ic_cls  = health_cls_inv(int_cov, 1.5, 3.0)
roe_cls = health_cls_inv(roe_v, 0.05, 0.12)
om_cls  = health_cls_inv(om_v, 0.05, 0.12)
nm_cls  = health_cls_inv(nm_v, 0.03, 0.08)
fcf_cls = "m-good" if fcf_v and fcf_v>0 else ("m-bad" if fcf_v and fcf_v<0 else "")

h1,h2,h3,h4=st.columns(4)
for col,cls,lbl,val,sub in[
    (h1,de_cls,"⚖️ Debt/Equity",f"{de_v/100:.2f}x" if de_v else "N/A","< 1x good · >2x risky"),
    (h2,cr_cls,"💧 Current Ratio",f"{cr_v:.2f}x" if cr_v else "N/A","< 1 = liquidity risk"),
    (h3,ic_cls,"🔒 Interest Coverage",f"{int_cov:.2f}x" if int_cov else "N/A","< 1.5x = danger zone"),
    (h4,fcf_cls,"💸 Free Cash Flow",fmt_cr(fcf_v),"Operating CF - Capex"),
]:
    with col: st.markdown(mc(cls,lbl,val,sub),unsafe_allow_html=True)

st.markdown("<div style='height:.4rem'></div>",unsafe_allow_html=True)
h5,h6,h7,h8=st.columns(4)
for col,cls,lbl,val,sub in[
    (h5,roe_cls,"📈 ROE",fmt_pct(roe_v),"> 15% strong"),
    (h6,"","📊 ROA",fmt_pct(roa_v),"Return on assets"),
    (h7,om_cls,"⚙️ Operating Margin",fmt_pct(om_v),"Core business efficiency"),
    (h8,nm_cls,"🏁 Net Margin",fmt_pct(nm_v),"Bottom line profitability"),
]:
    with col: st.markdown(mc(cls,lbl,val,sub),unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  GROWTH — Revenue + Net Profit YoY
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label growth">Revenue & Profit Growth</div>',unsafe_allow_html=True)

if not fin.empty:
    g1,g2=st.columns(2)

    def growth_bar(df, metric_keys, title, color, unit="Cr"):
        for key in metric_keys:
            if key in df.index:
                s = df.loc[key].dropna().sort_index()
                yrs = [d.strftime("%Y") for d in s.index]
                vals = s.values/1e7
                colors = ["rgba(239,68,68,0.7)" if v<0 else color for v in vals]
                fig = go.Figure(go.Bar(
                    x=yrs, y=vals,
                    marker=dict(color=colors,line=dict(width=0)),
                    hovertemplate=f"<b>%{{x}}</b><br>₹%{{y:,.2f}} {unit}<extra></extra>",
                ))
                yoy = []
                for i in range(1,len(vals)):
                    if vals[i-1]!=0: yoy.append(f"{((vals[i]-vals[i-1])/abs(vals[i-1])*100):+.1f}%")
                fig.update_layout(**{**PLOT_BASE,"yaxis":{**PLOT_BASE["yaxis"],"tickprefix":"₹","ticksuffix":f" {unit}"}},
                    title=dict(text=title,font=dict(size=13,color="#94a3b8"),x=0),height=260)
                st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>',unsafe_allow_html=True)
                return
        st.info(f"{title} data not available.")

    with g1: growth_bar(fin,["Total Revenue","Revenue"],"📦 Annual Revenue","rgba(56,189,248,0.7)")
    with g2: growth_bar(fin,["Net Income","Net Income Common Stockholders"],"💰 Annual Net Profit","rgba(16,185,129,0.7)")
else:
    st.info("Financial statement data not available for this stock.")

# ─────────────────────────────────────────────────────
#  OWNERSHIP
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label owner">Ownership Structure</div>',unsafe_allow_html=True)

own_shown = False
if holders is not None:
    try:
        insider_raw  = str(holders.iloc[0,0])
        inst_raw     = str(holders.iloc[1,0])
        insider_pct  = float(insider_raw.replace("%","").strip())
        inst_pct     = float(inst_raw.replace("%","").strip())
        retail_pct   = max(0, 100 - insider_pct - inst_pct)

        fig_own = go.Figure()
        for label,val,color in[
            ("Promoter / Insiders",insider_pct,"rgba(129,140,248,0.8)"),
            ("Institutions (FII+DII)",inst_pct,"rgba(56,189,248,0.8)"),
            ("Retail / Others",retail_pct,"rgba(100,116,139,0.6)"),
        ]:
            fig_own.add_trace(go.Bar(
                name=label, x=[val], y=["Holding"],
                orientation="h", text=f"{val:.1f}%", textposition="inside",
                marker_color=color,
                hovertemplate=f"<b>{label}</b>: {val:.1f}%<extra></extra>",
            ))
        fig_own.update_layout(
            barmode="stack", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,15,30,0.4)",
            height=100, margin=dict(l=0,r=0,t=10,b=10),
            xaxis=dict(range=[0,100],showgrid=False,showticklabels=False,zeroline=False),
            yaxis=dict(showgrid=False,showticklabels=False),
            showlegend=True, legend=dict(orientation="h",yanchor="bottom",y=1.02,font=dict(color="#94a3b8",size=11)),
            font=dict(family="DM Sans",color="#94a3b8"),
        )
        st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
        st.plotly_chart(fig_own,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>',unsafe_allow_html=True)
        own_shown=True
    except: pass
if not own_shown:
    st.info("Ownership data not available via Yahoo Finance for this stock. Check NSE/BSE for shareholding pattern.")

# ─────────────────────────────────────────────────────
#  ANALYST VIEW — Target + Reasons + History
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label analyst">Analyst View</div>', unsafe_allow_html=True)

tgt_mean  = safe(info, "targetMeanPrice")
tgt_high  = safe(info, "targetHighPrice")
tgt_low   = safe(info, "targetLowPrice")
rec_key   = safe(info, "recommendationKey", "")
n_analyst = safe(info, "numberOfAnalystOpinions", 0)
upside    = ((tgt_mean - curr_p) / curr_p * 100) if tgt_mean and curr_p else None

REC = {
    "strong_buy":  ("Strong Buy ⬆️",  "#10b981", "rgba(16,185,129,0.15)"),
    "buy":         ("Buy 🟢",          "#34d399", "rgba(52,211,153,0.12)"),
    "hold":        ("Hold ⬛",          "#fbbf24", "rgba(251,191,36,0.12)"),
    "sell":        ("Sell 🔴",          "#f97316", "rgba(249,115,22,0.12)"),
    "strong_sell": ("Strong Sell ⬇️",  "#ef4444", "rgba(239,68,68,0.15)"),
}
rec_label, rec_col, rec_bg = REC.get(rec_key, ("No Rating", "#64748b", "rgba(100,116,139,0.1)"))

if tgt_mean:
    # ── Target cards ──────────────────────────────────
    a1, a2, a3, a4 = st.columns(4)
    upside_cls = "m-good" if upside and upside > 10 else ("m-warn" if upside and upside > 0 else "m-bad")
    for col, cls, lbl, val, sub in [
        (a1, "",          "🎯 Mean Target",  fmt_price(tgt_mean),  f"{n_analyst} analyst(s)"),
        (a2, "m-good",    "⬆ High Target",  fmt_price(tgt_high),  "Bull case"),
        (a3, "m-bad",     "⬇ Low Target",   fmt_price(tgt_low),   "Bear case"),
        (a4, upside_cls,  "📐 Upside",       f"{upside:+.1f}%" if upside else "N/A", "vs current price"),
    ]:
        with col: st.markdown(mc(cls, lbl, val, sub), unsafe_allow_html=True)

    # ── Recommendation badge ───────────────────────────
    st.markdown(
        f'<div style="margin-top:.8rem;padding:.8rem 1.2rem;background:{rec_bg};border-radius:12px;'
        f'border:1px solid {rec_col}30;display:inline-flex;align-items:center;gap:.8rem">'
        f'<span style="color:{rec_col};font-size:1.1rem;font-weight:700">{rec_label}</span>'
        f'<span style="color:#475569;font-size:.8rem">Analyst consensus · {n_analyst} covering</span></div>',
        unsafe_allow_html=True
    )

    # ── Why this target? Auto-generated reasons ────────
    st.markdown(
        '<div style="color:#334155;font-size:.65rem;letter-spacing:2px;text-transform:uppercase;'
        'font-weight:700;margin:1.4rem 0 .7rem;padding-left:10px;border-left:3px solid #fbbf24">'
        'Why analysts set this target</div>',
        unsafe_allow_html=True
    )
    reasons = generate_analyst_reasons(info)
    r_cols  = st.columns(len(reasons))
    for col, (icon, title, desc) in zip(r_cols, reasons):
        with col:
            st.markdown(
                f'<div class="m-card" style="height:auto;padding:1rem 1.1rem">'
                f'<div style="font-size:1.3rem;margin-bottom:.4rem">{icon}</div>'
                f'<div style="color:#e2e8f0;font-size:.82rem;font-weight:700;margin-bottom:.35rem">{title}</div>'
                f'<div style="color:#475569;font-size:.72rem;line-height:1.5">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Upgrade / Downgrade History ─────────────────────
    if not upgrades_df.empty:
        st.markdown(
            '<div style="color:#334155;font-size:.65rem;letter-spacing:2px;text-transform:uppercase;'
            'font-weight:700;margin:1.4rem 0 .7rem;padding-left:10px;border-left:3px solid #fbbf24">'
            'Recent Analyst Actions</div>',
            unsafe_allow_html=True
        )
        GRADE_COL = {"Buy":"#10b981","Strong Buy":"#10b981","Outperform":"#34d399",
                     "Overweight":"#34d399","Neutral":"#fbbf24","Hold":"#fbbf24",
                     "Underperform":"#f97316","Sell":"#ef4444","Strong Sell":"#ef4444"}

        for _, row in upgrades_df.iterrows():
            try:
                dt    = pd.to_datetime(row.get("GradeDate","")).strftime("%d %b %Y")
            except: dt = "—"
            firm  = row.get("Firm","—")
            tog   = str(row.get("ToGrade",""))
            frm   = str(row.get("FromGrade",""))
            action= str(row.get("Action",""))
            col_  = GRADE_COL.get(tog, "#64748b")
            frm_html = f' <span style="color:#334155">from {frm}</span>' if frm and frm != "nan" else ""
            act_icon = "⬆️" if "up" in action.lower() else ("⬇️" if "down" in action.lower() else "➡️")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:1rem;padding:.55rem .8rem;'
                f'background:#0d1117;border:1px solid #1e293b;border-radius:10px;margin-bottom:.4rem">'
                f'<span style="color:#334155;font-size:.72rem;min-width:80px">{dt}</span>'
                f'<span style="color:#64748b;font-size:.8rem;font-weight:600;flex:1">{firm}</span>'
                f'<span style="color:{col_};font-size:.82rem;font-weight:700">{act_icon} {tog}{frm_html}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
else:
    st.info("No analyst coverage data available for this stock.")

# ─────────────────────────────────────────────────────
#  NEWS FEED
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label news_">Latest News</div>',unsafe_allow_html=True)

if news_items:
    for item in news_items:
        title   = item.get("title","")
        pub     = item.get("publisher","")
        link    = item.get("link","#")
        ts_news = item.get("providerPublishTime",0)
        dt_str  = datetime.fromtimestamp(ts_news).strftime("%d %b %Y") if ts_news else ""
        st.markdown(f'''<a href="{link}" target="_blank" style="text-decoration:none"><div class="news-item"><div class="news-title">{title}</div><div class="news-meta">{pub} &nbsp;·&nbsp; {dt_str}</div></div></a>''',unsafe_allow_html=True)
else:
    st.info("No recent news available.")

# ─────────────────────────────────────────────────────
#  HISTORICAL OVERVIEW
# ─────────────────────────────────────────────────────
ath=float(hist["High"].max()); ath_d=hist["High"].idxmax().strftime("%d %b %Y")
atl=float(hist["Low"].min());  atl_d=hist["Low"].idxmin().strftime("%d %b %Y")
ld=hist.index[0].strftime("%d %b %Y"); lp=float(hist["Close"].iloc[0]); lv=int(hist["Volume"].iloc[0])

st.markdown('<div class="section-label hist">Historical Overview — Since Listing</div>',unsafe_allow_html=True)
hc1,hc2,hc3,hc4=st.columns(4)
for col,extra,lbl,val,sub in[
    (hc1,"","📅 Listing Date",ld,"First day on NSE"),
    (hc2,"","💰 Listing Price",fmt_price(lp),f"Vol: {fmt_vol(lv)}"),
    (hc3,"hist-card-high","🏆 All-Time High",fmt_price(ath),ath_d),
    (hc4,"hist-card-low","📉 All-Time Low",fmt_price(atl),atl_d),
]:
    with col: st.markdown(f'<div class="hist-card {extra}"><div class="hist-card-lbl">{lbl}</div><div class="hist-card-val">{val}</div><div class="hist-card-sub">{sub}</div></div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  HISTORICAL CHARTS — shared frequency selector
# ─────────────────────────────────────────────────────
st.markdown('<div class="section-label hist">Historical Charts</div>',unsafe_allow_html=True)

freq = st.radio("",list(TIMEFRAMES.keys()),index=3,horizontal=True,label_visibility="collapsed",key="freq_sel")
hist_view = load_period(ticker, TIMEFRAMES[freq])

# Price
st.markdown('<div style="color:#64748b;font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .4rem;font-weight:600">Price History</div>',unsafe_allow_html=True)
fig_p=go.Figure(go.Scatter(x=hist_view.index,y=hist_view["Close"],mode="lines",line=dict(color="#38bdf8",width=1.8),fill="tozeroy",fillcolor="rgba(56,189,248,0.05)",hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.2f}<extra></extra>"))
fig_p.update_layout(**PLOT_BASE,height=300)
st.markdown('<div class="chart-wrap">',unsafe_allow_html=True); st.plotly_chart(fig_p,use_container_width=True,config={"displayModeBar":False}); st.markdown('</div>',unsafe_allow_html=True)

# Volume
st.markdown('<div style="color:#64748b;font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .4rem;font-weight:600">Volume History</div>',unsafe_allow_html=True)
bar_colors=["rgba(16,185,129,0.65)" if c>=o else "rgba(239,68,68,0.65)" for c,o in zip(hist_view["Close"],hist_view["Open"])]
fig_v=go.Figure(go.Bar(x=hist_view.index,y=hist_view["Volume"],marker=dict(color=bar_colors,line=dict(width=0)),hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:,} shares<extra></extra>"))
vl2={**PLOT_BASE,"yaxis":{**PLOT_BASE["yaxis"],"tickprefix":""}}
fig_v.update_layout(**vl2,height=230)
st.markdown('<div class="chart-wrap">',unsafe_allow_html=True); st.plotly_chart(fig_v,use_container_width=True,config={"displayModeBar":False}); st.markdown('</div>',unsafe_allow_html=True)
st.markdown('<div style="display:flex;gap:1.5rem;padding:.4rem .3rem 0"><span style="color:#6ee7b7;font-size:.75rem;font-weight:600">🟢 Up Day</span><span style="color:#fca5a5;font-size:.75rem;font-weight:600">🔴 Down Day</span></div>',unsafe_allow_html=True)

# P/E
# P/E gets its own frequency selector
pe_freq = st.radio("",list(TIMEFRAMES.keys()),index=3,horizontal=True,
    label_visibility="collapsed",key="pe_freq_sel")
hist_pe_view = load_period(ticker, TIMEFRAMES[pe_freq])

if pe_series is not None and not pe_series.empty:
    cutoff   = hist_pe_view.index[0] if not hist_pe_view.empty else pe_series.index[0]
    pe_view  = pe_series[pe_series.index>=cutoff].dropna()
    if not pe_view.empty:
        pe_mean=float(pe_view.mean()); pe_max=float(pe_view.max()); pe_min=float(pe_view.min())
        st.markdown('<div style="color:#64748b;font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .4rem;font-weight:600">P/E Ratio History</div>',unsafe_allow_html=True)
        fig_pe=go.Figure(go.Scatter(x=pe_view.index,y=pe_view,mode="lines",line=dict(color="#c084fc",width=1.8),fill="tozeroy",fillcolor="rgba(192,132,252,0.06)",hovertemplate="<b>%{x|%d %b %Y}</b><br>P/E: %{y:.2f}x<extra></extra>"))
        fig_pe.add_hline(y=pe_mean,line_dash="dot",line_color="rgba(251,191,36,0.5)",annotation_text=f"Avg {pe_mean:.1f}x",annotation_font_color="#fbbf24",annotation_position="bottom right")
        pe_layout={**PLOT_BASE,"yaxis":{**PLOT_BASE["yaxis"],"tickprefix":"","ticksuffix":"x"},"height":260}
        fig_pe.update_layout(**pe_layout)
        st.markdown('<div class="chart-wrap">',unsafe_allow_html=True); st.plotly_chart(fig_pe,use_container_width=True,config={"displayModeBar":False}); st.markdown('</div>',unsafe_allow_html=True)
        st.markdown(f'<div style="display:flex;gap:2rem;padding:.4rem .3rem 0"><span style="color:#c084fc;font-size:.75rem;font-weight:600">Avg: {pe_mean:.1f}x</span><span style="color:#6ee7b7;font-size:.75rem;font-weight:600">Min: {pe_min:.1f}x</span><span style="color:#fca5a5;font-size:.75rem;font-weight:600">Max: {pe_max:.1f}x</span></div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────
st.markdown(f"""<div class="dash-footer">Data via Yahoo Finance · Live price every 3s · Buy/Sell estimated from price-position · For analysis only, not financial advice<br>Loaded: {datetime.now().strftime('%d %b %Y, %H:%M:%S')} IST</div>""",unsafe_allow_html=True)
