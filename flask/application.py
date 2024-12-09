from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
from functions import (
    calculate_sell_dollars,
    calculate_sell_value,
    calculate_buy_cost,
    calculate_profit,
    adjust_profit_for_fees,
    split_profit,
)

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            initial_dollars REAL,
            buy_rate REAL,
            dollars_left REAL,
            sell_dollars REAL,
            sell_rate REAL,
            sell_value REAL,
            buy_cost REAL,
            profit REAL,
            reserved_fee REAL,
            final_profit REAL,
            sultan_share REAL,
            shahzad_share REAL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get the inputs from the form
            date = request.form['date']  # Get the date input from the form
            initial_dollars = float(request.form['initial_dollars'])
            buy_rate = float(request.form['buy_rate'])
            dollars_left = float(request.form['dollars_left'])
            sell_rate = float(request.form['sell_rate'])
            reserved_fee = float(request.form['reserved_fee'])

            # Debugging: print received form data
            print(f"Date: {date}, Initial Dollars: {initial_dollars}, Buy Rate: {buy_rate}, "
                  f"Dollars Left: {dollars_left}, Sell Rate: {sell_rate}, Reserved Fee: {reserved_fee}")

            # Validation check
            if initial_dollars < dollars_left:
                return "❗ Dollars left cannot exceed initial dollars. Please check your inputs."

            # Perform the calculations
            sell_dollars = calculate_sell_dollars(initial_dollars, dollars_left)
            sell_value = calculate_sell_value(sell_dollars, sell_rate)
            buy_cost = calculate_buy_cost(sell_dollars, buy_rate)
            profit = calculate_profit(buy_cost, sell_value)
            final_profit = adjust_profit_for_fees(profit, reserved_fee, sell_rate)
            sultan_share, shahzad_share = split_profit(final_profit)
            

            # Debugging: print calculated values
            print(f"Sell Dollars: {sell_dollars}, Sell Value: {sell_value}, Buy Cost: {buy_cost}, "
                  f"Profit: {profit}, Final Profit: {final_profit}, Sultan Share: {sultan_share}, Shahzad Share: {shahzad_share}")

            # Save the record to the database, including the user-provided date
            conn = sqlite3.connect('transactions.db')
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO transactions (initial_dollars, buy_rate, dollars_left, sell_dollars, sell_rate, sell_value,
                                          buy_cost, profit, reserved_fee, final_profit, sultan_share, shahzad_share, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (initial_dollars, buy_rate, dollars_left, sell_dollars, sell_rate, sell_value,
                  buy_cost, profit, reserved_fee, final_profit, sultan_share, shahzad_share, date))
            conn.commit()
            conn.close()

            # Display the results
            return render_template('index.html', 
                                   sell_dollars=sell_dollars, 
                                   sell_value=sell_value, 
                                   buy_cost=buy_cost, 
                                   profit=profit, 
                                   reserved_fee=reserved_fee,
                                   final_profit=final_profit,
                                   sultan_share=sultan_share, 
                                   shahzad_share=shahzad_share)
        except Exception as e:
            # Print the error for debugging
            print("Error:", e)
            return f"❗ An error occurred during the calculation. Error: {e}"

    return render_template('index.html')













@app.route('/total_profits', methods=['GET', 'POST'])
def total_profits():
    total_profit = 0
    if request.method == 'POST':
        # Get form data
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        person = request.form['person']

        # Validate person input
        if person not in ['sultan', 'shahzad']:
            return "❗ Invalid person selected. Please choose either Sultan or Shahzad."

        # Database query to fetch profit sum based on person and date range
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()

        if person == 'sultan':
            cursor.execute(''' 
                SELECT SUM(sultan_share) FROM transactions 
                WHERE date BETWEEN ? AND ?
            ''', (start_date, end_date))
        elif person == 'shahzad':
            cursor.execute(''' 
                SELECT SUM(shahzad_share) FROM transactions 
                WHERE date BETWEEN ? AND ?
            ''', (start_date, end_date))

        result = cursor.fetchone()
        conn.close()

        # If there's no result, default to 0
        if result and result[0] is not None:
            total_profit = result[0]
        else:
            total_profit = 0

    return render_template('total_profits.html', total_profit=total_profit)











# Route to show the database content
@app.route('/view_transactions', methods=['GET'])
def view_transactions():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()

    return render_template('view_transactions.html', transactions=transactions)




if __name__ == '__main__':
    init_db()  # Initialize the database before starting the app
    app.run(debug=True)
