def calculate_sell_dollars(initial_dollars, dollars_left):
    """Calculate the dollars sold by subtracting the dollars left from initial dollars."""
    return initial_dollars - dollars_left

def calculate_sell_value(sell_dollars, sell_rate):
    """Calculate the value obtained from selling dollars."""
    return sell_dollars * sell_rate

def calculate_buy_cost(sell_dollars, buy_rate):
    """Calculate the cost of buying dollars."""
    return sell_dollars * buy_rate

def calculate_profit(buy_cost, sell_value):
    """Calculate the profit from selling dollars."""
    return sell_value - buy_cost

def adjust_profit_for_fees(profit, reserved_fee, sell_rate):
    """Adjust profit by subtracting the reserved fees."""
    return profit - (reserved_fee * sell_rate)

def split_profit(profit):
    """Split the profit into Sultan's and Shahzad's shares."""
    sultan_share = 0.3 * profit
    shahzad_share = 0.7 * profit
    return sultan_share, shahzad_share
