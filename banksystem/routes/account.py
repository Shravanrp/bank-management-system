from flask import Blueprint, render_template, session, redirect, request, url_for,flash
from banksystem.db import get_db
from datetime import datetime,timedelta
import math

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/create', methods=['GET', 'POST'])
def create_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()

    cur.execute("SELECT * FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    if cur.fetchone():
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        acc_type = request.form['account_type']
        balance = float(request.form['balance'])
        cur.execute("INSERT INTO ACCOUNT (C_ID, Acc_type, Bal) VALUES (%s, %s, %s)",
                    (customer['C_Id'], acc_type, balance))
        conn.commit()
        return redirect(url_for('dashboard.dashboard'))

    return render_template('create_account.html')
@account_bp.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()
    if not customer:
        return redirect(url_for('dashboard.dashboard'))
    cur.execute("SELECT Bal FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    accounts=cur.fetchone()
    cur.execute("SELECT Acc_no FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    account_nos = [row['Acc_no'] for row in cur.fetchall()]
    transactions = []
    if account_nos:
        format_strings = ','.join(['%s'] * len(account_nos))
        cur.execute(f"SELECT * FROM TRANSACTIONS WHERE Acc_no IN ({format_strings}) ORDER BY Date DESC, Time DESC", tuple(account_nos))
        transactions = cur.fetchall()

    return render_template('transactions.html', transactions=transactions,accounts=accounts)

@account_bp.route('/loans')
def loans():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()
    if not customer:
        return redirect(url_for('dashboard.dashboard'))

    cur.execute("SELECT * FROM LOAN WHERE C_ID = %s ORDER BY S_date DESC", (customer['C_Id'],))
    loans = cur.fetchall()

    return render_template('loans.html', loans=loans)
@account_bp.route('/apply_loan', methods=['GET', 'POST'])
def apply_loan():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()
    if not customer:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        loan_type = request.form['loan_type']
        amount = float(request.form['amount'])
        duration_months = int(request.form['duration'])

        annual_interest_rate = 10.0
        monthly_interest_rate = annual_interest_rate / (12 * 100)

        r = monthly_interest_rate
        n = duration_months
        emi = (amount * r * (1 + r)**n) / ((1 + r)**n - 1)
        emi = round(emi, 2)

        s_date = datetime.today().date()
        e_date = s_date + timedelta(days=30*n) 

        cur.execute("""
            INSERT INTO LOAN (C_ID, Loan_type, Amount, Interest, EMI, S_date, E_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            customer['C_Id'], loan_type, amount,
            annual_interest_rate, emi, s_date, e_date
        ))
        conn.commit()

        return redirect(url_for('account.loans'))

    return render_template('apply_loan.html')
@account_bp.route('/transaction', methods=['GET', 'POST'])
def do_transaction():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()
    if not customer:
        flash("Customer not found.")
        return redirect(url_for('dashboard.dashboard'))

    cur.execute("SELECT * FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    account = cur.fetchone()
    if not account:
        flash("You must create an account first.")
        return redirect(url_for('account.create_account'))

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            trans_type = request.form['trans_type']
        except (ValueError, KeyError):
            flash("Invalid input.")
            return redirect(request.url)

        current_balance = float(account['Bal'])

        if amount <= 0:
            flash("Amount must be greater than 0.")
            return redirect(request.url)

        if trans_type == 'Withdraw' and amount > current_balance:
            flash("Insufficient balance.")
            return redirect(request.url)

        new_balance = current_balance + amount if trans_type == 'Deposit' else current_balance - amount

        cur.execute("""
            INSERT INTO TRANSACTIONS (C_ID, Acc_no, Trans_type, Amount, Date, Time)
            VALUES (%s, %s, %s, %s, CURDATE(), CURTIME())
        """, (customer['C_Id'], account['Acc_no'], trans_type, amount))

        # Update balance
        cur.execute("UPDATE ACCOUNT SET Bal = %s WHERE Acc_no = %s", (new_balance, account['Acc_no']))
        conn.commit()

        flash(f"{trans_type} of ₹{amount:.2f} successful.")
        return redirect(url_for('account.transactions'))

    return render_template('do_transaction.html', account=account)