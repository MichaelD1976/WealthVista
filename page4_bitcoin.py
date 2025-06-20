import streamlit as st
import pandas as pd
# import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.optimize import curve_fit



def main():
    
    st.header("Bitcoin Power Law Trend", divider='blue')
    st.write("""
    Bitcoin's price has historically followed a power law trend with remarkable consistency, 
            evidenced by a coefficient of determination (R²) of 0.96, indicating an incredibly strong regression fit. 
            This high R² suggests that Bitcoin's growth pattern is not random but follows a statistically robust trajectory. 
            The trend reflects how Bitcoin’s network effects (in user adoption and hash rate growth) are scaling in proportion to time.
            This trend was first identified by physicist Giovanni Santostasi. For more information please check out his youtube channel: https://www.youtube.com/@quantonomy
            
            """)
    st.write("")


    # Load the Bitcoin data
    df = pd.read_csv("data/raw/bitcoin_historical_dataset_raw.csv")
    df.rename(columns={'Start': 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Convert dates to numeric ordinal format for regression
    df['Date_ordinal'] = df['Date'].map(lambda x: x.toordinal())  # Dates as ordinals (numeric)

    # Scale down the Date_ordinal to avoid overflow
    min_date = df['Date_ordinal'].min()  # Get the earliest date
    df['Scaled_Date'] = df['Date_ordinal'] - min_date  # Subtract min date to scale the dates

    # Prepare data for power law fitting (Date as numeric, Close as price)
    X = df['Scaled_Date'].values  # Scaled Dates
    y = df['Close'].values  # Bitcoin closing prices

    # Define a power law function (y = a * x^b)
    def power_law(x, a, b):
        return a * (x ** b)

    # Fit the power law to the data
    params, covariance = curve_fit(power_law, X, y)

    # Extract fitted parameters (a and b)
    a = params[0]
    b = params[1]

    # Calculate the fitted power trend line (y = a * x^b)
    df['Power_Trend'] = a * (df['Scaled_Date'] ** b)  # Apply the power law formula to get trend values

    # Calculate upper and lower bounds based on the inverse multipliers
    upper_multiplier = 1.80
    lower_multiplier = 1 / upper_multiplier  # This is 0.555
    df['Power_Trend_Upper'] = df['Power_Trend'] * upper_multiplier  # Upper bound (1.80 times the trend)
    df['Power_Trend_Lower'] = df['Power_Trend'] * lower_multiplier  # Lower bound (0.555 times the trend)

    # Streamlit slider for years of future projection
    # Y-axis scale selector in the Streamlit sidebar or main area
    with st.sidebar:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.title('Plot Filters')
        y_axis_type = st.sidebar.selectbox("Y-axis Scale", ["log", "linear"])
        years_to_project = st.sidebar.slider("Years to project into future", 1, 20, 5)

    # Function to generate future dates (extended trend for given years)
    def generate_future_dates(years):
        future_dates = pd.date_range(df['Date'].max(), periods=years * 365, freq='D')  # Approx 365 days per year
        future_scaled_dates = (future_dates.map(lambda x: x.toordinal()) - min_date)  # Convert future dates to ordinal format
        future_trend_values = a * (future_scaled_dates ** b)  # Predict future values using power law
        # Apply the inverse multipliers for future bounds
        future_trend_upper = future_trend_values * upper_multiplier  # Upper bound for future (1.80 times the trend)
        future_trend_lower = future_trend_values * lower_multiplier  # Lower bound for future (0.555 times the trend)
        return future_dates, future_trend_values, future_trend_upper, future_trend_lower

    future_dates, future_trend_values, future_trend_upper, future_trend_lower = generate_future_dates(years_to_project)

    # Create figure
    fig = go.Figure()

    # Add traces for actual data and trends
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Close"], mode='lines', name="Bitcoin Price", line=dict(color='cyan')
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Power_Trend"], mode='lines', name="Power Trend", line=dict(color='red', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Power_Trend_Upper"], mode='lines', name="Upper Trend + 80%", line=dict(color='green', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Power_Trend_Lower"], mode='lines', name="Lower Trend - 55.55%", line=dict(color='blue', dash='dot')
    ))

    # Extended future trends
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_trend_values, mode='lines', name="Power Trend", line=dict(color='red', dash='dot'), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_trend_upper, mode='lines', name="Trend + 80%", line=dict(color='green', dash='dot'), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_trend_lower, mode='lines', name="Trend - 55.55%", line=dict(color='blue', dash='dot'), showlegend=False
    ))

    # Halving event dates with vertical dashed lines
    halving_dates = ["2012-11-01", "2016-07-01", "2020-05-01", "2024-04-01", "2028-03-01"]
    halving_dates = [pd.to_datetime(date) for date in halving_dates]
    for date in halving_dates:
        fig.add_shape(
            type="line", x0=date, x1=date, y0=0, y1=1, yref="paper",
            line=dict(color="gray", width=1, dash="dash")
        )
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="lines", name="Bitcoin Halvings",
        line=dict(color="gray", width=1, dash="dash")
    ))



    # Layout tweaks for dark theme and interactivity
    fig.update_layout(
        height=700,  # Taller chart
        title={
            'text': "Bitcoin Price Over Time with Power Trend and Bounds",
            'font': {'color': 'white', 'size': 22},  # Larger white title
            'x': 0.5,  # Center title
            'xanchor': 'center'
        },
        legend=dict(
            font=dict(color='white'),
            bgcolor='#121212',  # Match dark background
            bordercolor='gray',
            borderwidth=0.5
        ),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikedash="solid",
            spikecolor="white",
            spikethickness=1,
            gridcolor="#444"
        ),
        yaxis=dict(
            showspikes=True,
            spikemode="across",
            spikedash="solid",
            spikecolor="white",
            spikethickness=1,
            gridcolor="#444"
            # 'type' is removed here; handled via Streamlit control
        )
    )


    # Apply selected scale to the chart
    fig.update_yaxes(type=y_axis_type)

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    st.caption('''
    On a linear chart, Bitcoin’s price history appears chaotic. But when viewed through the lens of a logarithmic scale, a strikingly consistent and elegant growth pattern emerges — revealing a long-term trajectory that is remarkably constrained.

    ''')


    # -------------------------------------
    st.write("")
    st.write("")
    st.write("")

    with st.expander('Bitcoin Power Law Retirement Calculator'):

        st.header("📈 Bitcoin Retirement Calculator")
        st.caption("Estimates when your Bitcoin holdings will be worth enough to retire based on a continued power law trend")

        # --- User Inputs ---
        btc_holdings = st.number_input("Enter your Bitcoin holdings (BTC):", min_value=0.0, value=0.2, step=0.01)
        annual_expenses = st.number_input("Your annual living expenses in today's money (£/$):", min_value=0, value=30000, step=1000)
        expected_growth_percent = st.number_input(
            "Assumed annual BTC growth rate (%) - based on the power law, Bitcoin's growth is projected to average more than 20% annually for a multi-decade period", 
            min_value=1, max_value=100, value=30, step=1
        )

        try:
            expected_growth = 1 + (expected_growth_percent / 100)
            
            # Derive retirement multiplier from growth rate (e.g., 25% → 4 times)
            # Formula: multiplier = 1 / (growth_rate - 1)
            retirement_multiplier = 1 / (expected_growth - 1)

            retirement_target = annual_expenses * retirement_multiplier
            target_price_per_btc = retirement_target / btc_holdings

            # Calculate scaled ordinal date using power law inverse
            scaled_date_target = (target_price_per_btc / a) ** (1 / b)
            retirement_ordinal = int(scaled_date_target + min_date)

            if retirement_ordinal > datetime.date.max.toordinal():
                st.error("🚫 Projected retirement date exceeds maximum supported date.")
            else:
                retirement_date = datetime.date.fromordinal(retirement_ordinal)
                today = datetime.date.today()
                if retirement_date <= today:
                    st.success("🎉 You can already retire based on your BTC holdings and retirement target!")
                else:
                    st.success(f"🎯 Estimated retirement date based on power law trend: **{retirement_date.strftime('%Y-%m-%d')}**")
                    st.info(f"ℹ️ Retirement target is set to {retirement_multiplier:.2f} times your annual expenses based on {expected_growth_percent}% growth and withdrawal rate.")

        except Exception as e:
            st.error(f"Error calculating retirement date: {e}")


        # st.write('Based on drawing down 20% of holdings per year with an expected power law growth curve in excess of this')
        st.caption('Not financial advice 😉')

if __name__ == '__main__':
    main()










