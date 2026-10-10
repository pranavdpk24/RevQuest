
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import yfinance as yf

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="RevQuest | Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM DESIGN
# ==================================================

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    [data-testid="stHeader"] {
        background-color: rgba(11, 17, 32, 0.95);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .brand-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #60a5fa;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .brand-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }

    .section-heading {
        color: #f3f4f6;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stMetric"] {
        background-color: #111c30;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 20px 18px;
    }

    [data-testid="stMetricLabel"] {
        color: #9ca3af;
    }

    [data-testid="stMetricValue"] {
        color: #f9fafb;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 700;
        min-height: 45px;
        width: 100%;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #3b82f6;
        color: white;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #111c30;
        border-color: #374151;
        border-radius: 8px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #263449;
        border-radius: 10px;
        overflow: hidden;
    }

    .info-panel {
        background-color: #111c30;
        border: 1px solid #263449;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 14px 16px;
        color: #cbd5e1;
        margin-bottom: 1rem;
    }

    .footer-text {
        color: #6b7280;
        font-size: 0.85rem;
        text-align: center;
        padding-top: 1.5rem;
    }

    hr {
        border-color: #263449;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR: USER CONTROLS
# ==================================================

with st.sidebar:
    st.markdown(
        "<div class='brand-title'>📈 RevQuest</div>",
        unsafe_allow_html=True
    )

    st.caption("STOCK MARKET ANALYTICS")

    st.divider()

    st.subheader("Dashboard Settings")

    ticker = st.text_input(
        "Stock ticker",
        value="AAPL",
        help="Examples: AAPL, MSFT, GOOGL, AMZN"
    ).strip().upper()

    period = st.selectbox(
        "Historical time period",
        ["1mo", "3mo", "6mo", "1y", "5y"],
        index=3,
        format_func=lambda value: {
            "1mo": "1 Month",
            "3mo": "3 Months",
            "6mo": "6 Months",
            "1y": "1 Year",
            "5y": "5 Years"
        }[value]
    )

    forecast_days = st.selectbox(
        "Forecast length",
        [7, 30, 90],
        index=1,
        format_func=lambda days: f"{days} business days"
    )

    st.divider()

    get_data = st.button(
        "Load Stock Dashboard",
        type="primary",
        use_container_width=True
    )

    st.caption(
        "Data source: Yahoo Finance via yfinance"
    )

    st.caption(
        "Forecasts are mathematical estimates, "
        "not guaranteed market predictions."
    )

# ==================================================
# MAIN DASHBOARD HEADER
# ==================================================

st.markdown(
    "<div class='brand-title'>RevQuest</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='brand-subtitle'>"
    "Explore stock performance, historical trends, "
    "and estimated future prices."
    "</div>",
    unsafe_allow_html=True
)

st.divider()

# Load data only after the user clicks the button.
if get_data:

    if not ticker:
        st.warning("Please enter a stock ticker.")

    else:
        try:
            with st.spinner(
                f"Loading market data for {ticker}..."
            ):
                stock = yf.Ticker(ticker)
                data = stock.history(period=period)

            if data.empty:
                st.error(
                    "No stock data was found. "
                    "Check the ticker and try again."
                )

            else:
                prices = data["Close"].dropna()

                if prices.empty:
                    st.error(
                        "No valid closing prices were found."
                    )

                else:
                    # --------------------------------------
                    # CALCULATE STOCK METRICS
                    # --------------------------------------

                    starting_price = float(prices.iloc[0])
                    latest_close = float(prices.iloc[-1])

                    absolute_change = (
                        latest_close - starting_price
                    )

                    percentage_change = (
                        absolute_change / starting_price
                    ) * 100 if starting_price != 0 else 0

                    # --------------------------------------
                    # PERFORMANCE OVERVIEW
                    # --------------------------------------

                    st.markdown(
                        "<div class='section-heading'>"
                        "Performance Overview"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    st.caption(
                        f"{ticker} · "
                        f"Historical period: {period}"
                    )

                    metric1, metric2, metric3, metric4 = (
                        st.columns(4)
                    )

                    metric1.metric(
                        "Latest Close",
                        f"${latest_close:,.2f}"
                    )

                    metric2.metric(
                        "Starting Close",
                        f"${starting_price:,.2f}"
                    )

                    metric3.metric(
                        "Price Change",
                        f"${absolute_change:+,.2f}"
                    )

                    metric4.metric(
                        "Period Change",
                        f"{percentage_change:+.2f}%",
                        delta=f"{percentage_change:+.2f}%"
                    )

                    st.divider()

                    # --------------------------------------
                    # HISTORICAL PRICE CHART
                    # --------------------------------------

                    st.markdown(
                        "<div class='section-heading'>"
                        "Historical Performance"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    chart_data = data.reset_index()

                    date_column = (
                        "Date"
                        if "Date" in chart_data.columns
                        else "Datetime"
                    )

                    chart_data[date_column] = (
                        pd.to_datetime(
                            chart_data[date_column],
                            utc=True
                        ).dt.tz_localize(None)
                    )

                    historical_fig = go.Figure()

                    historical_fig.add_trace(
                        go.Scatter(
                            x=chart_data[date_column],
                            y=chart_data["Close"],
                            mode="lines",
                            name="Closing Price",
                            line=dict(
                                color="#60a5fa",
                                width=2.5
                            ),
                            fill="tozeroy",
                            fillcolor="rgba(96,165,250,0.08)"
                        )
                    )

                    historical_fig.update_layout(
                        title=dict(
                            text=f"{ticker} Closing Price",
                            font=dict(size=19)
                        ),
                        paper_bgcolor="#0b1120",
                        plot_bgcolor="#0b1120",
                        font=dict(
                            color="#d1d5db",
                            family="Arial"
                        ),
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        hovermode="x unified",
                        margin=dict(
                            l=20,
                            r=20,
                            t=65,
                            b=20
                        ),
                        xaxis=dict(
                            showgrid=False,
                            zeroline=False
                        ),
                        yaxis=dict(
                            gridcolor="#263449",
                            zeroline=False,
                            tickprefix="$"
                        ),
                        showlegend=False
                    )

                    st.plotly_chart(
                        historical_fig,
                        width="stretch"
                    )

                    # --------------------------------------
                    # ESTIMATED FUTURE PRICES
                    # --------------------------------------

                    st.markdown(
                        "<div class='section-heading'>"
                        "Estimated Future Prices"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        "<div class='info-panel'>"
                        "RevQuest uses a simple linear trend "
                        "based on up to the last 90 available "
                        "closing prices. This is for learning "
                        "and experimentation, not a reliable "
                        "prediction of future market prices."
                        "</div>",
                        unsafe_allow_html=True
                    )

                    recent_prices = prices.tail(90)

                    if len(recent_prices) < 2:
                        st.warning(
                            "There is not enough historical "
                            "data to calculate a forecast."
                        )

                    else:
                        recent_dates = pd.DatetimeIndex(
                            recent_prices.index
                        )

                        if recent_dates.tz is not None:
                            recent_dates = (
                                recent_dates.tz_localize(None)
                            )

                        last_date = recent_dates[-1]

                        y_values = recent_prices.to_numpy(
                            dtype=float
                        )

                        forecast_dates = pd.bdate_range(
                            start=(
                                last_date
                                + pd.offsets.BDay(1)
                            ),
                            periods=forecast_days
                        )

                        x_values = np.arange(
                            len(recent_prices)
                        )

                        model = np.polyfit(
                            x_values,
                            y_values,
                            1
                        )

                        future_x = np.arange(
                            len(recent_prices),
                            len(recent_prices) + forecast_days
                        )

                        forecast_values = np.polyval(
                            model,
                            future_x
                        )

                        forecast_values = np.maximum(
                            forecast_values,
                            0
                        )

                        forecast_fig = go.Figure()

                        forecast_fig.add_trace(
                            go.Scatter(
                                x=recent_dates,
                                y=y_values,
                                mode="lines",
                                name="Historical",
                                line=dict(
                                    color="#60a5fa",
                                    width=2.5
                                )
                            )
                        )

                        forecast_fig.add_trace(
                            go.Scatter(
                                x=[last_date] + list(
                                    forecast_dates
                                ),
                                y=[
                                    float(
                                        recent_prices.iloc[-1]
                                    )
                                ] + forecast_values.tolist(),
                                mode="lines+markers",
                                name="Estimated",
                                line=dict(
                                    color="#fbbf24",
                                    width=2.5,
                                    dash="dash"
                                ),
                                marker=dict(size=5)
                            )
                        )

                        forecast_fig.update_layout(
                            title=dict(
                                text=(
                                    f"{ticker} — "
                                    f"{forecast_days}-Business-Day "
                                    "Estimate"
                                ),
                                font=dict(size=19)
                            ),
                            paper_bgcolor="#0b1120",
                            plot_bgcolor="#0b1120",
                            font=dict(
                                color="#d1d5db",
                                family="Arial"
                            ),
                            xaxis_title="Date",
                            yaxis_title="Price (USD)",
                            hovermode="x unified",
                            margin=dict(
                                l=20,
                                r=20,
                                t=65,
                                b=20
                            ),
                            xaxis=dict(
                                showgrid=False
                            ),
                            yaxis=dict(
                                gridcolor="#263449",
                                tickprefix="$"
                            ),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )

                        st.plotly_chart(
                            forecast_fig,
                            width="stretch"
                        )

                        forecast_table = pd.DataFrame({
                            "Date": forecast_dates.strftime(
                                "%Y-%m-%d"
                            ),
                            "Estimated Price (USD)": [
                                round(float(price), 2)
                                for price in forecast_values
                            ]
                        })

                        with st.expander(
                            "View forecast data",
                            expanded=True
                        ):
                            st.dataframe(
                                forecast_table,
                                width="stretch",
                                hide_index=True
                            )

                        st.caption(
                            "Forecast dates exclude weekends "
                            "but may include market holidays."
                        )

                    st.divider()

                    # --------------------------------------
                    # HISTORICAL DATA TABLE
                    # --------------------------------------

                    st.markdown(
                        "<div class='section-heading'>"
                        "Historical Data"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    with st.expander(
                        "View historical records",
                        expanded=False
                    ):
                        display_data = chart_data.copy()

                        display_data[date_column] = (
                            display_data[date_column].astype(str)
                        )

                        st.dataframe(
                            display_data,
                            width="stretch",
                            hide_index=True
                        )

                    # --------------------------------------
                    # FOOTER
                    # --------------------------------------

                    st.divider()

                    st.markdown(
                        "<div class='footer-text'>"
                        "RevQuest | Built with Python, "
                        "Streamlit, Plotly, Pandas, NumPy "
                        "and yfinance.<br>"
                        "For educational purposes only. "
                        "Not financial advice."
                        "</div>",
                        unsafe_allow_html=True
                    )

        except Exception as error:
            st.error(
                "We couldn't retrieve the stock data. "
                "Check your internet connection and ticker, "
                "then try again."
            )

            st.caption(
                f"Technical details: {error}"
            )

else:
    # Initial screen before a stock is loaded
    st.markdown(
        "<div class='info-panel'>"
        "👈 Enter a stock ticker in the sidebar, "
        "choose your time periods, and click "
        "<b>Load Stock Dashboard</b> to get started."
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("### What you can explore")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.markdown("#### 📊 Performance")
        st.write(
            "Explore closing prices and changes "
            "over your selected historical period."
        )

    with feature2:
        st.markdown("#### 📈 Price Trends")
        st.write(
            "View historical prices and a simple "
            "mathematical forecast."
        )

    with feature3:
        st.markdown("#### 🗂️ Data Tables")
        st.write(
            "Inspect the historical records and "
            "estimated future prices."
        )
