import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go






def main():

    st.header('Portfolio Accumulation Projections', divider='blue')
    st.write('Enter inputs and adjust any defaulted growth rate assumptions to desired estimates. Projection table and plot will automatically update.')
    cl_one, _ = st.columns([1,9])
    with cl_one:
        denom = st.selectbox('Select Denomination:', ['£', '$'])


    # ----------------------------  INPUTS  --------------------------------

    col1, col2, col3 = st.columns([5,0.5,5])
    with col1:
        with st.container(border=True):
            st.subheader("Portfolio Inputs")
            current_value = st.number_input(f'Enter Current Portfolio Valuation {denom}', min_value = 0, value = 10000)

            stocks_weight = st.slider('Enter Approximate Portfolio Stocks %', min_value = 0, max_value = 100, value = 70, step = 1, key='stocks_weight')
            bonds_weight = st.slider('Enter Approximate Portfolio Bonds %', min_value = 0, max_value = 100, value = 20, step = 1, key='bonds_weight')
            property_weight = st.slider('Enter Approximate Portfolio Property %', min_value = 0, max_value = 100, value = 5, step = 1, key='property_weight')
            cash_weight = st.slider('Enter Approximate Portfolio Cash %', min_value = 0, max_value = 100, value = 3, step = 1, key='cash_weight')
            btc_weight = st.slider('Enter Approximate Portfolio Bitcoin %', min_value = 0, max_value = 100, value = 2, step = 1, key='btc_weight')

            total_weights = stocks_weight + bonds_weight + property_weight + cash_weight + btc_weight 
            if total_weights != 100:
                st.warning(f"%'s need to sum to 100, currently {total_weights}")
                st.stop()
            else:
                pass

            annual_contribution = st.number_input(f'Enter Annual Contribution {denom}', min_value = 0, value = 3000)

            num_years = st.slider("Select Number of Years to Project", 0, 50, 30, step=10, key="num_year")


    st.subheader("Optional: Lump Sum Contributions")

    possible_lump_sum = st.checkbox('Enable Lump Sum Additions/Withdrawals')

    # Initialize lump sums in session state
    if possible_lump_sum:
        if 'lump_sums' not in st.session_state:
            st.session_state.lump_sums = []

        # Form to add new lump sum
        with st.form(key='lump_sum_form', clear_on_submit=True):
            lump_amount = st.number_input(
                'Enter Lump Sum Amount (use negative for withdrawal)',
                min_value=-10_000_000,  # ✅ Allows negative entries
                max_value=10_000_000,
                value=0,
                step=1000,
                help="Use a negative value for a withdrawal"
            )
            lump_year = st.number_input('Enter Year of Lump Sum (e.g. 3 = year 3)', min_value=1)
            add_lump = st.form_submit_button('Apply Lump Sum')

            if add_lump and lump_amount != 0:
                st.session_state.lump_sums.append({'Year': lump_year, 'Amount': lump_amount})

        # Show and manage lump sum table
        if st.session_state.lump_sums:
            st.write("Scheduled Lump Sums:")
            lump_df = pd.DataFrame(st.session_state.lump_sums)

            # Add delete buttons per row
            for i, row in lump_df.iterrows():
                col1, col2, _ = st.columns([6, 1, 1])
                with col1:
                    st.write(f"Year {row['Year']}, Amount: {denom}{row['Amount']:,.0f}")
                with col2:
                    if st.button(f"❌ Remove", key=f"remove_{i}"):
                        st.session_state.lump_sums.pop(i)
                        st.rerun()

            # Add reset button
            if st.button("🧹 Clear All Lump Sums"):
                st.session_state.lump_sums = []
                st.rerun()


    with col3:
        with st.container(border=True):
            st.subheader('Annual Asset Class % Growth Rate Assumptions')
            st.write("Default values are inflation adjusted long term estimates")
            st.write("")
            st.write("")
            st.write("")
            stocks_growth = st.slider('Stocks', 0,10,5)
            bonds_growth = st.slider('Bonds', 0,10,2)
            proprty_growth = st.slider('Property', 0,10,2)
            cash_growth = st.slider('Cash',0,10,0)
            btc_growth = st.slider('Bitcoin', 0,40,20)


    st.write("---")
    # -------------------------  OUTPUTS  --------------------------------------

    if (stocks_weight + bonds_weight + property_weight + cash_weight + btc_weight == 100) and current_value > 0:


        # Asset weights and growth rates in %
        weights = {
            'Stocks': stocks_weight / 100,
            'Bonds': bonds_weight / 100,
            'Property': property_weight / 100,
            'Cash': cash_weight / 100,
            'Bitcoin': btc_weight / 100
        }

        growth_rates = {
            'Stocks': stocks_growth / 100,
            'Bonds': bonds_growth / 100,
            'Property': proprty_growth / 100,
            'Cash': cash_growth / 100,
            'Bitcoin': btc_growth / 100
        }

        # Convert lump sums to dictionary {year: total lump}
        lump_sum_map = {}
        if possible_lump_sum and 'lump_sums' in st.session_state:
            for item in st.session_state.lump_sums:
                lump_sum_map[item['Year']] = lump_sum_map.get(item['Year'], 0) + item['Amount']


        # Initialize projection DataFrame
        projection_data = []

        start_value = current_value

        # Projection loop
        for year in range(1, num_years + 1):
            year_data = {'Year': year, 'Start Value': start_value}

            # Apply any lump sum start this year
            lump_sum = lump_sum_map.get(year, 0)
            year_data['Lump Sum'] = lump_sum
            start_value += lump_sum

            total_growth = 0

            for asset in weights:
                asset_value = start_value * weights[asset]
                asset_growth = asset_value * growth_rates[asset]

                year_data[f'{asset} Value'] = asset_value
                year_data[f'{asset} Growth'] = asset_growth

                total_growth += asset_growth

            # Add growth and standard contribution
            year_data['Growth'] = total_growth
            year_data['Contribution'] = annual_contribution

            # Calculate end value
            year_data['End Value'] = start_value + total_growth + annual_contribution

            start_value = year_data['End Value']
            projection_data.append(year_data)

        # Create DataFrame
        df_projection = pd.DataFrame(projection_data)
        df_projection_2 = df_projection.set_index('Year') # for display (index become year)

        # Display with formatting
        st.subheader("Projection Table")
        st.caption("Asset allocation rebalancing occurs at the end of each year")
        st.dataframe(
            df_projection_2.style.format({col: f'{denom}{{:,.0f}}' for col in df_projection.columns})
        )

    else:
        st.info("Enter all inputs and ensure weights sum to 100 to view projection.")


    # ----------------------  PLOT  --------------------------

    # Calculate cumulative value per asset per year prior to plotting

    df_cumulative = df_projection[['Year']].copy()

    for asset in weights:
        # Each asset's cumulative value is its base value + growth added each year
        df_cumulative[asset] = df_projection[f'{asset} Value'] + df_projection[f'{asset} Growth']

    # Optionally recalculate to reflect contributions/lump sums split per weight (advanced)
    # For now, we just stack what's tracked per asset in `df_projection`

    # Melt for Plotly
    df_long = df_cumulative.melt(id_vars='Year', var_name='Asset Class', value_name='Value')

    # Add total for overlay
    df_cumulative['Total'] = df_projection['End Value']




    # Prepare DataFrame for plot
    # We'll calculate the cumulative growth per asset per year (stacked area chart)
    assets = list(weights.keys())
    df_plot = df_projection[['Year'] + [f'{asset} Growth' for asset in assets]].copy()
    df_plot['End Value'] = df_projection['End Value']

    # Melt the dataframe to long format for Plotly
    df_melted = df_plot.melt(id_vars='Year', 
                            value_vars=[f'{asset} Growth' for asset in assets],
                            var_name='Asset Class', 
                            value_name='Growth Amount')

    # Clean the 'Asset Class' names
    df_melted['Asset Class'] = df_melted['Asset Class'].str.replace(' Growth', '')


    # Stacked area chart of cumulative values
    fig = px.area(
        df_long,
        x='Year',
        y='Value',
        color='Asset Class',
        title="",
        labels={'Value': 'Value (£)'},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # Add End Value line
    fig.add_trace(
        go.Scatter(
            x=df_cumulative['Year'],
            y=df_cumulative['Total'],
            mode='lines+markers',
            name='Total Portfolio Value',
            line=dict(color='black', width=2),
            marker=dict(size=6),
            hovertemplate='Year: %{x}<br>Total Value: £%{y:,.0f}<extra></extra>'
        )
    )

    # Layout tweaks
    fig.update_layout(
        hovermode='x unified',
        legend_title='Asset Class',
        margin=dict(l=40, r=40, t=60, b=40),
        height=600,
        plot_bgcolor='rgba(95, 95, 95, 0.95)',
        # paper_bgcolor='rgba(95, 95, 95, 0.10)',
        xaxis=dict(title='Year', showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(title='Portfolio Value (£)', tickprefix='£', separatethousands=True, showgrid=True, gridcolor='lightgrey'),
    )

    st.write("")
    st.subheader('Portfolio & Asset Growth Over Time')

    final_value = int(df_projection['End Value'].iloc[-1])
    annual_contribution_abs = abs(int(annual_contribution))

    if denom == '$':
        display_denom = '\\$'  # escape dollar sign
    else:
        display_denom = denom

    st.write(
    f'Given annual contributions of {display_denom}{annual_contribution_abs:,} per year, chosen asset allocations and a starting portfolio of {display_denom}{current_value:,}, '
    f"after {num_years} years the final portfolio is projected to reach **{display_denom}{final_value:,}** in today's purchasing power given real (inflation-adjusted) growth "
    f'from total contributions of {denom}{(annual_contribution * num_years):,}.'
    )

    st.plotly_chart(fig, use_container_width=True)









if __name__ == '__main__':
    main()