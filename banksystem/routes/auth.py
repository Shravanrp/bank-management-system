from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from banksystem.db import get_db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    session.clear()
    return render_template('home.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        minit = request.form.get('minit', '')
        address = request.form['address']
        phone = request.form['phone']
        b_id = 1

        if not (email and password and fname and lname and address and phone):
            flash("All fields are required.", "error")
            return redirect(url_for('auth.register'))

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM USERS WHERE Email = %s", (email,))
            if cur.fetchone():
                flash("Email already registered.", "error")
                return redirect(url_for('auth.register'))

            hashed_pw = generate_password_hash(password)
            cur.execute("INSERT INTO USERS (Email, Password) VALUES (%s, %s)", (email, hashed_pw))
            conn.commit()
            user_id = cur.lastrowid

            cur.execute(
                "INSERT INTO CUSTOMERS (B_Id, User_Id, Fname, Minit, Lname, Address, Ph_no) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (b_id, user_id, fname, minit, lname, address, phone)
            )
            conn.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            conn.rollback()
            flash("Registration failed. Please try again.", "error")
            current_app.logger.error(f"Registration error: {e}")
            return redirect(url_for('auth.register'))
    return render_template('register.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM USERS WHERE Email = %s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['Password'], password):
            session.permanent = True
            session['user_id'] = user['User_Id']
            session['email'] = user['Email']
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid credentials.", "error")
    return render_template('login.html')
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))
