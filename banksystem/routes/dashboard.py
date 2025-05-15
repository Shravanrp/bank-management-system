from flask import Blueprint, render_template, session, redirect, url_for
from banksystem.db import get_db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()

    cur.execute("SELECT * FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    account = cur.fetchone()

    if not account:
        return redirect(url_for('account.create_account'))

    return render_template('dashboard.html', customer=customer, account=account)
