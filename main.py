import streamlit as st

st.set_page_config(layout="wide")

def main():

    st.sidebar.title('Menu')

    page_options = [
        'Home',
        'Accumulation',
        'Drawdown',
        'Bitcoin Power Law',
        'Asset Growth Comparisons',
    ]

    selected_page = st.sidebar.selectbox("Select a page", options=page_options, key="selected_page")

    if selected_page == 'Home':
        st.title("📈 WealthVista")
        st.subheader("Wealth Accumulation & Retirement Drawdown Projection Tool")


        st.markdown(
            """
            <hr style="border: 1px solid #007BFF;">

            **WealthVista** is a financial projection tool designed to help individuals model long-term **investment accumulation** and **retirement drawdown** scenarios with clarity and flexibility.

            ### What It Does
            This app allows you to:
            - Simulate how your investments might grow over time with custom asset allocations and annual contributions
            - Explore the impact of **market returns**, **contributions**, and **one-time lump sums** (deposits or withdrawals)
            - Visualise drawdown phases to see how **regular withdrawals** affect the portfolio over retirement
            - Switch between accumulation and drawdown phases to gain a full-picture understanding of your WealthVista

            ### How It Helps
            Whether you're **planning for retirement**, testing different asset allocation strategies, or managing withdrawals in later life, **WealthVista** gives you insight into:
            - The long-term sustainability of your portfolio
            - When and how wealth peaks and declines
            - The effects of different asset growth characteristics, compounding and strategic allocation decisions

            Get started by selecting **Accumulation** or **Drawdown** from the sidebar to begin your personalized projection.

            <hr style="border: 1px solid #007BFF;">
            """,
            unsafe_allow_html=True
        )

    if selected_page == 'Accumulation':
        import page2_accumulation
        page2_accumulation.main()

    elif selected_page == 'Drawdown':
        import page3_drawdown
        page3_drawdown.main()

    elif selected_page == 'Bitcoin Power Law':
        import page4_bitcoin
        page4_bitcoin.main()

    elif selected_page == 'Asset Growth Comparisons':
        import page5_charts
        page5_charts.main()


if __name__ == '__main__':
    main()




