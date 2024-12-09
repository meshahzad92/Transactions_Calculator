import streamlit as st
from functions import (
    calculate_sell_dollars,
    calculate_sell_value,
    calculate_buy_cost,
    calculate_profit,
    adjust_profit_for_fees,
    split_profit,
)

st.set_page_config(page_title="Dollar Transaction Calculator", page_icon="💵", layout="wide")

def main():
    st.title("💵 Dollar Transaction Calculator")
    st.markdown(
        """
        Welcome to the **Dollar Transaction Calculator**. Use this app to easily calculate profits from dollar transactions and split them proportionally between Sultan and Shahzad.
        """
    )

    st.sidebar.title("🔧 Input Parameters")
    st.sidebar.markdown("Provide the details of your transaction below:")

    # Step 1: Ask for initial dollars in account
    initial_dollars = st.sidebar.number_input(
        "💼 Initial dollars in your account:", min_value=0.0, step=0.01, format="%.2f"
    )

    # Step 2: Ask for the buy rate of dollars
    buy_rate = st.sidebar.number_input(
        "📉 Buy rate of dollars:", min_value=0.0, step=0.01, format="%.2f"
    )

    # Step 3: Ask for how much dollars are now left in Binance
    dollars_left = st.sidebar.number_input(
        "📊 Dollars left in Binance:", min_value=0.0, step=0.01, format="%.2f"
    )

    if initial_dollars < dollars_left:
        st.error("❗ Dollars left cannot exceed initial dollars. Please check your inputs.")
        return

    # Step 4: Calculate the sell dollars
    sell_dollars = calculate_sell_dollars(initial_dollars, dollars_left)

    # Display results dynamically
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Dollars Sold", value=f"{sell_dollars:.2f}$")

    # Step 5: Ask for the sell rate of dollars
    sell_rate = st.sidebar.number_input(
        "💵 Sell rate of dollars:", min_value=0.0, step=0.01, format="%.2f"
    )

    if sell_rate > 0 and sell_dollars > 0:
        # Step 6: Calculate the value obtained from selling dollars
        sell_value = calculate_sell_value(sell_dollars, sell_rate)
        
        buy_cost = calculate_buy_cost(sell_dollars, buy_rate)

        profit = calculate_profit(buy_cost, sell_value)
        reserved_fee = st.sidebar.number_input(
            "💰 Reserved fee (in dollars):", min_value=0.0, step=0.01, format="%.2f"
        )

        final_profit = adjust_profit_for_fees(profit, reserved_fee, sell_rate)
        sultan_share, shahzad_share = split_profit(final_profit)

        with col2:
            st.metric(label="Final Profit After Fees", value=f"{final_profit:.2f}rs")

        st.markdown(
            """
            ### Profit Distribution in 
            - **Sultan's Share (30%)**: {:.2f}rs
            - **Shahzad's Share (70%)**: {:.2f}rs
            """.format(sultan_share, shahzad_share)
        )

        st.balloons()
    else:
        st.warning("⚠️ Ensure the sell rate and dollars sold are greater than zero.")

if __name__ == "__main__":
    main()
