import json
from datetime import datetime

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

from tools.registry import ToolRegistry
from tools.yahoo_tool import YahooFinanceTool
from tools.tavily_tool import TavilyTool
from tools.sec_tool import SECTool
from tools.scraper_tool import ScraperTool
from tools.company_profile_tool import CompanyProfileTool
from tools.financial_calculator_tool import FinancialCalculatorTool
from tools.technical_indicator_tool import TechnicalIndicatorTool
from tools.stock_comparison_tool import StockComparisonTool
from tools.currency_converter_tool import CurrencyConverterTool
from tools.earnings_calendar_tool import EarningsCalendarTool
from agents.research_agent import ResearchAgent


st.set_page_config(
    page_title="QUANT DESK | Financial Research Agent",
    page_icon="📈",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def get_agent():
    registry = ToolRegistry()
    registry.register(YahooFinanceTool())
    registry.register(TavilyTool())
    registry.register(SECTool())
    registry.register(ScraperTool())
    registry.register(CompanyProfileTool())
    registry.register(FinancialCalculatorTool())
    registry.register(TechnicalIndicatorTool())
    registry.register(StockComparisonTool())
    registry.register(CurrencyConverterTool())
    registry.register(EarningsCalendarTool())
    return ResearchAgent(registry), registry


def fmt_money(value):
    if value is None:
        return "N/A"
    try:
        value = float(value)
        if value >= 1e12:
            return f"${value / 1e12:.2f}T"
        if value >= 1e9:
            return f"${value / 1e9:.2f}B"
        if value >= 1e6:
            return f"${value / 1e6:.2f}M"
        return f"${value:,.2f}"
    except Exception:
        return "N/A"


def infer_recommendation(report: str):
    text = report.lower()

    if "strong buy" in text:
        return "STRONG BUY", "#00D97E"
    if "buy" in text or "outperform" in text:
        return "BUY", "#00D97E"
    if "hold" in text or "neutral" in text:
        return "HOLD", "#FFB020"
    if "sell" in text or "avoid" in text:
        return "SELL", "#FF4D5E"

    return "REVIEW", "#4D9FFF"


def get_tool_data(result, tool_name):
    """
    Safely extract tool data.
    Always returns a dictionary.
    Never returns None.
    """

    try:
        tool_results = result.get("tool_results", {})

        if not isinstance(tool_results, dict):
            return {}

        tool_result = tool_results.get(tool_name, {})

        if not isinstance(tool_result, dict):
            return {}

        data = tool_result.get("data", {})

        if data is None:
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    except Exception:
        return {}


def render_price_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        if hist.empty:
            st.info("No chart data available.")
            return

        fig = go.Figure()

        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                name=ticker,
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            margin=dict(l=10, r=10, t=40, b=10),
            title=f"{ticker} 6-Month Price Chart",
            xaxis_rangeslider_visible=False,
            paper_bgcolor="#12171C",
            plot_bgcolor="#12171C",
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.info("Chart could not be loaded.")


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg:#0A0E12;
    --card:#12171C;
    --card2:#161C22;
    --border:#1E2630;
    --text:#E8EDF2;
    --muted:#8A96A3;
    --green:#00D97E;
    --red:#FF4D5E;
    --amber:#FFB020;
    --blue:#4D9FFF;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(0,217,126,0.08), transparent 35%),
        radial-gradient(circle at 90% 10%, rgba(77,159,255,0.08), transparent 35%),
        var(--bg);
    color: var(--text);
}

#MainMenu, footer, header {
    visibility:hidden;
}

.block-container {
    max-width: 1320px;
    padding-top: 1rem;
}

* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
}

.hero {
    border:1px solid var(--border);
    background: linear-gradient(135deg, rgba(0,217,126,0.10), rgba(77,159,255,0.08), rgba(18,23,28,1));
    border-radius:18px;
    padding:30px;
    margin-bottom:20px;
}

.hero h1 {
    font-size:42px;
    margin-bottom:6px;
}

.hero p {
    color:var(--muted);
    font-size:15px;
}

.card {
    background: var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:22px;
    margin-bottom:16px;
}

.kpi {
    background: var(--card);
    border:1px solid var(--border);
    border-radius:14px;
    padding:18px;
}

.kpi-label {
    font-size:12px;
    color:var(--muted);
    text-transform:uppercase;
    letter-spacing:1.5px;
}

.kpi-value {
    font-size:24px;
    font-weight:800;
    color:var(--text);
    margin-top:6px;
}

.rec-card {
    border-radius:18px;
    padding:28px;
    border:1px solid var(--border);
    background: linear-gradient(135deg, rgba(0,217,126,0.12), rgba(18,23,28,1));
}

.report-box {
    background: #0F141A;
    border:1px solid var(--border);
    border-radius:16px;
    padding:30px;
    line-height:1.75;
}

.news-card {
    background: var(--card);
    border:1px solid var(--border);
    border-radius:14px;
    padding:18px;
    margin-bottom:12px;
}

.badge {
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    background:rgba(0,217,126,0.10);
    color:var(--green);
    font-weight:700;
    font-size:12px;
    margin-right:6px;
}

.stButton button {
    background: var(--green) !important;
    color:#06140D !important;
    border:none !important;
    border-radius:10px !important;
    font-weight:800 !important;
}

.stTextInput input {
    background: var(--card2) !important;
    color: var(--text) !important;
    border:1px solid var(--border) !important;
    border-radius:10px !important;
}

section[data-testid="stSidebar"] {
    background: var(--card);
    border-right:1px solid var(--border);
}
</style>
""",
    unsafe_allow_html=True,
)


agent, registry = get_agent()

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []


with st.sidebar:
    st.markdown("## 📡 QUANT DESK")
    st.caption("Autonomous Financial Research Agent")
    st.markdown("---")

    st.markdown("### ✅ Tools Online")
    for tool in registry.list_tools():
        st.markdown(f"🟢 `{tool}`")

    st.markdown("---")
    st.markdown("### Session History")

    if not st.session_state.history:
        st.caption("No research yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(
                f"{item.get('ticker', '—')} · {item.get('query', '')[:24]}",
                key=f"h{i}",
            ):
                st.session_state.result = item


st.markdown(
    """
<div class="hero">
    <span class="badge">AI RESEARCH SYSTEM</span>
    <span class="badge">10 TOOLS</span>
    <span class="badge">3-LAYER MEMORY</span>
    <h1>Financial Research Agent</h1>
    <p>
    Ask about any company, stock, market trend, SEC filing, latest news, or investment opportunity.
    The agent plans research, gathers evidence, synthesizes findings, and produces a professional investment report.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


col_q, col_b = st.columns([5, 1])

with col_q:
    query = st.text_input(
        "Research Query",
        placeholder="Example: Analyze NVIDIA stock using latest news and SEC filing",
        label_visibility="collapsed",
    )

with col_b:
    run = st.button("RUN AGENT ▸", use_container_width=True)


example_cols = st.columns(4)

examples = [
    "Analyze Apple stock using latest news and SEC filing",
    "Compare Apple and Microsoft as long-term investments",
    "Analyze NVIDIA and its AI growth opportunity",
    "Analyze whether Tesla is overvalued",
]

for col, ex in zip(example_cols, examples):
    with col:
        if st.button(ex, use_container_width=True):
            query = ex
            run = True


if run and query.strip():
    with st.status("Agent running...", expanded=True) as status:
        st.write("📋 Planning research...")
        st.write("🧰 Calling financial tools...")
        st.write("🔬 Synthesizing evidence...")

        result = agent.run(query)

        st.write("✅ Report ready.")
        status.update(
            label="Research complete",
            state="complete",
            expanded=False,
        )

    st.session_state.result = result
    st.session_state.history.append(result)


result = st.session_state.result


if result is None:
    st.markdown(
        """
<div class="card" style="text-align:center;padding:70px;">
    <h2>📈 Ready to Research</h2>
    <p style="color:#8A96A3;">Enter a financial research question above to begin.</p>
</div>
""",
        unsafe_allow_html=True,
    )

else:
    ticker = result.get("ticker", "—")
    report = result.get("report", "")
    evaluation = result.get("evaluation", {}) or {}
    tool_results = result.get("tool_results", {}) or {}

    recommendation, rec_color = infer_recommendation(report)

    yahoo_data = get_tool_data(result, "yahoo_finance") or {}
    profile_data = get_tool_data(result, "company_profile") or {}
    calc_data = get_tool_data(result, "financial_calculator") or {}
    tech_data = get_tool_data(result, "technical_indicator") or {}

    st.markdown(
        f"""
<div class="rec-card">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:20px;">
        <div>
            <div style="color:#8A96A3;font-size:13px;letter-spacing:2px;">INVESTMENT VIEW</div>
            <h1 style="color:{rec_color};font-size:58px;margin:0;">{recommendation}</h1>
            <p style="color:#8A96A3;">
                Ticker: <b>{ticker}</b> · Quality Score: <b>{evaluation.get("quality_score", "N/A")}%</b>
            </p>
        </div>
        <div style="font-size:76px;">📊</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
<div class='kpi'>
    <div class='kpi-label'>Current Price</div>
    <div class='kpi-value'>{fmt_money(yahoo_data.get('current_price'))}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
<div class='kpi'>
    <div class='kpi-label'>Market Cap</div>
    <div class='kpi-value'>{fmt_money(yahoo_data.get('market_cap'))}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
<div class='kpi'>
    <div class='kpi-label'>P/E Ratio</div>
    <div class='kpi-value'>{yahoo_data.get('pe_ratio', 'N/A')}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
<div class='kpi'>
    <div class='kpi-label'>Trend Signal</div>
    <div class='kpi-value'>{tech_data.get('trend_signal', 'N/A')}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("")

    tab_overview, tab_report, tab_news, tab_chart, tab_advanced = st.tabs(
        [
            "⭐ Overview",
            "📄 Full Report",
            "📰 News",
            "📈 Chart",
            "🧠 Advanced Analysis",
        ]
    )

    with tab_overview:
        c1, c2 = st.columns([1.2, 1])

        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Company Snapshot")
            st.write(f"**Company:** {profile_data.get('company', 'N/A')}")
            st.write(f"**Sector:** {profile_data.get('sector', 'N/A')}")
            st.write(f"**Industry:** {profile_data.get('industry', 'N/A')}")
            st.write(f"**CEO:** {profile_data.get('ceo', 'N/A')}")
            st.write(f"**Employees:** {profile_data.get('employees', 'N/A')}")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Calculated Insights")

            profit_margin = calc_data.get("profit_margin_percent")
            if profit_margin is None:
                st.write("**Profit Margin:** N/A")
            else:
                st.write(f"**Profit Margin:** {profit_margin}%")

            st.write(f"**Price-to-Sales:** {calc_data.get('price_to_sales') or 'N/A'}")
            st.write(f"**Valuation View:** {calc_data.get('valuation') or 'N/A'}")
            st.write(f"**SMA 20:** {tech_data.get('sma_20') or 'N/A'}")
            st.write(f"**SMA 50:** {tech_data.get('sma_50') or 'N/A'}")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Why this output is useful")
        st.markdown(
            """
- Combines live market data, SEC filing metadata, web news, technical signals, and AI synthesis.
- Gives a clear recommendation-style view first.
- Keeps advanced technical details available for verification.
- Allows report download for submission or presentation.
"""
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_report:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(report)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇ Download Research Report",
            data=report,
            file_name=f"{ticker}_research_report.md",
            mime="text/markdown",
        )

    with tab_news:
        tavily_result = tool_results.get("tavily", {})
        news_items = tavily_result.get("data", []) if isinstance(tavily_result, dict) else []

        if not news_items:
            st.info("No news results available.")
        else:
            for item in news_items[:5]:
                title = item.get("title", "Untitled")
                url = item.get("url", "")
                content = item.get("content", "")

                st.markdown(
                    f"""
<div class="news-card">
    <h4>{title}</h4>
    <p style="color:#8A96A3;">{content[:350]}...</p>
    <a href="{url}" target="_blank">Open Source ↗</a>
</div>
""",
                    unsafe_allow_html=True,
                )

    with tab_chart:
        render_price_chart(ticker)

    with tab_advanced:
        adv1, adv2 = st.tabs(["Agent Reasoning", "Raw Evidence"])

        with adv1:
            st.markdown("### Research Plan")
            st.code(json.dumps(result.get("plan", {}), indent=2), language="json")

            st.markdown("### ReAct Trace")
            for i, step in enumerate(result.get("react_steps", []), start=1):
                with st.expander(f"{i}. {step.get('action', '')}"):
                    st.code(
                        json.dumps(step, indent=2, default=str),
                        language="json",
                    )

            st.markdown("### Synthesis")
            st.code(
                json.dumps(result.get("synthesis", {}), indent=2, default=str),
                language="json",
            )

        with adv2:
            st.markdown("### Tool Results")
            st.code(
                json.dumps(tool_results, indent=2, default=str),
                language="json",
            )

            st.markdown("### Evaluation")
            st.code(
                json.dumps(evaluation, indent=2, default=str),
                language="json",
            )