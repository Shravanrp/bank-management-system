
# Bank Management System

A simple bank management system built using Flask, HTML, CSS, and MySQL (via XAMPP). The system includes features such as user authentication, bank account creation, loan applications, and transactions.

## 📋 Prerequisites

Make sure you have the following installed before proceeding:

- [Python (3.10 or later)](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 🔧 Setup Instructions

### 1. Create a Virtual Environment

Open your terminal or command prompt and run:

```bash
python -m venv venv
````

Activate the virtual environment:

* **Windows**:

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 2. Clone the Repository

```bash
git clone https://github.com/Shravanrp/bank-management-system.git
cd bank-management-system
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Install XAMPP

Download and install XAMPP from the official website:

🔗 [Download XAMPP](https://www.apachefriends.org/index.html)

### 5. Set Up the Database

1. Open **XAMPP Control Panel**.
2. Start **Apache** and **MySQL**.
3. Open **phpMyAdmin** by visiting:
   [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
4. Create a new database named: `bank`
5. Import the `bank_database_schema.sql` file located in the root of the project.

📺 **Need help with XAMPP setup?**
Watch this YouTube tutorial:
[How to Setup XAMPP and phpMyAdmin](https://www.youtube.com/watch?v=h6DEDm7C37A)

### 6. Run the Application

```bash
python run.py
```

Then, visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✨ Features

* ✅ User Authentication (Login/Register)
* 🏦 Create Bank Account
* 💸 Apply for a Loan
* 🔁 Do Transactions (Deposit/Withdraw)

## 🛠️ Technologies Used

* **Frontend**: HTML, CSS
* **Backend**: Python, Flask
* **Database**: MySQL (via XAMPP)

---

## 📁 Project Structure

```plaintext
bank-management-system/
│   run.py
│   requirements.txt
│   bank_database_schema.sql
│   ...
└───banksystem/
    ├───routes/
    ├───static/
    ├───templates/
    └───db.py
```

---
