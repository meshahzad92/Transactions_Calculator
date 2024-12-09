import streamlit as st
from functions import (
    calculate_sell_dollars,
    calculate_sell_value,
    calculate_buy_cost,
    calculate_profit,
    adjust_profit_for_fees,
    split_profit,
)

st.set_page_config(page_title="Dollar Transaction Calculator", page_icon="💵", layout="centered")

def main():
    st.title("💵 Dollar Transaction Calculator")
    st.markdown(
        """
        Welcome to the **Dollar Transaction Calculator**. Use this app to easily calculate profits from dollar transactions and split them proportionally between Sultan and Shahzad.
        """
    )

    # Sidebar for inputs
    st.sidebar.header("Transaction Inputs")

    # Step 1: Ask for initial dollars in account
    initial_dollars = st.sidebar.number_input(
        "Enter the initial dollars in your account:", min_value=0.0, step=0.01, format="%.2f"
    )

    # Step 2: Ask for the buy rate of dollars
    buy_rate = st.sidebar.number_input(
        "Enter the buy rate of dollars:", min_value=0.0, step=0.01, format="%.2f"
    )

    # Step 3: Ask for how much dollars are now left in Binance
    dollars_left = st.sidebar.number_input(
        "Enter the dollars left in Binance:", min_value=0.0, step=0.01, format="%.2f"
    )

    # Validation: Ensure inputs are valid
    if initial_dollars < dollars_left:
        st.error("Dollars left cannot exceed initial dollars. Please check your inputs.")
        return

    # Step 4: Calculate the sell dollars
    sell_dollars = calculate_sell_dollars(initial_dollars, dollars_left)
    st.metric(label="Dollars Sold", value=f"{sell_dollars:.2f}")

    # Step 5: Ask for the sell rate of dollars
    sell_rate = st.sidebar.number_input(
        "Enter the sell rate of dollars:", min_value=0.0, step=0.01, format="%.2f"
    )

    if sell_rate > 0 and sell_dollars > 0:
        # Step 6: Calculate the value obtained from selling dollars
        sell_value = calculate_sell_value(sell_dollars, sell_rate)
        st.metric(label="Value from Selling Dollars", value=f"{sell_value:.2f}")

        # Step 7: Calculate the cost of buying dollars
        buy_cost = calculate_buy_cost(sell_dollars, buy_rate)

        # Calculate the profit
        profit = calculate_profit(buy_cost, sell_value)
        st.metric(label="Profit Before Fees", value=f"{profit:.2f}")

        # Step 8: Ask for any reserved fees
        reserved_fee = st.sidebar.number_input(
            "Enter the reserved fee (in dollars):", min_value=0.0, step=0.01, format="%.2f"
        )

        # Step 9: Adjust profit for fees
        final_profit = adjust_profit_for_fees(profit, reserved_fee, sell_rate)
        st.metric(label="Final Profit After Fees", value=f"{final_profit:.2f}")

        # Step 10: Split the profit
        sultan_share, shahzad_share = split_profit(final_profit)
        st.markdown(
            """
            ### Profit Distribution
            - **Sultan's Profit (30%)**: ${:.2f}
            - **Shahzad's Profit (70%)**: ${:.2f}
            """.format(sultan_share, shahzad_share)
        )

        st.success("Calculation complete! Check your results above.")
    else:
        st.warning("Please ensure that the sell rate and dollars sold are greater than zero.")

if __name__ == "__main__":
    main()
