import streamlit as st
import pandas as pd
# import numpy as np
# import datetime
import plotly.graph_objects as go
# from scipy.optimize import curve_fit



def main():
    
    # import streamlit as st
    # import pandas as pd
    # import plotly.graph_objs as go


    # --- Title ---
    st.header("Asset Plots", divider='blue')
    st.write('Data since 2010. Data source: y-finance. Gold price is estimated from SPDR spot ETF prices')
    st.write("")

    # --- Load data ---
    @st.cache_data
    def load_data():
        df = pd.read_csv('data/processed/merged_prices.csv', parse_dates=['Date'])
        df.sort_values('Date', inplace=True)
        return df

    df = load_data()

    # --- Sidebar controls ---
    st.sidebar.header("Select Data to Plot")

    # Columns to show (excluding 'Date')
    price_columns = [col for col in df.columns if col != 'Date']

    # Multi-select box for user to pick which columns to plot
    selected_columns = st.sidebar.multiselect(
        "Choose assets to visualise:",
        price_columns,
        default=["S&P500_$", "Gold_Price_$"]
    )

    # --- Main plot section ---
    if selected_columns:
        fig = go.Figure()

        for col in selected_columns:
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            ))

        fig.update_layout(
            title="Selected Asset Prices Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified",
            plot_bgcolor="#1E1E1E",
            paper_bgcolor="#121212",
            template="plotly_dark",
            
            # Legend settings
            legend=dict(
                orientation="h",
                x=0.01,
                y=1.1,
                font=dict(color="white")  # <-- White legend text
            ),

            # Gridline & axis styling
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",  # Light vertical gridlines
                zeroline=False,
                showline=True,
                linecolor="rgba(255,255,255,0.2)",
                showspikes=True,
                spikemode="across",
                spikesnap="cursor",
                spikethickness=1,
                spikecolor="rgba(255,255,255,0.3)",  # Vertical hover line
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                zeroline=False,
                showline=True,
                linecolor="rgba(255,255,255,0.2)"
            ),

            margin=dict(l=60, r=40, t=80, b=60),  # Add margin to prevent touching edge
            height=600
)

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Please select at least one asset from the sidebar to plot.")

    # --- Optional: Show raw data ---
    st.write("")
    with st.expander("Show Raw Data"):
        st.dataframe(df)



    # -------------------------------------


if __name__ == '__main__':
    main()










