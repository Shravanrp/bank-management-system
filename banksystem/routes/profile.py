from flask import Blueprint, render_template, session, redirect, url_for
from banksystem.db import get_db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMERS WHERE User_Id = %s", (session['user_id'],))
    customer = cur.fetchone()
    cur.execute("SELECT * FROM ACCOUNT WHERE C_ID = %s", (customer['C_Id'],))
    account = cur.fetchone()

    return render_template('profile.html', customer=customer, account=account)
