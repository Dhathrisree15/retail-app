from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'retail2024'

def load_data():
    conn = sqlite3.connect('retail.db')
    hh = pd.read_csv('400_households.csv')
    tx = pd.read_csv('400_transactions.csv')
    pr = pd.read_csv('400_products.csv')
    hh.columns = hh.columns.str.strip()
    tx.columns = tx.columns.str.strip()
    pr.columns = pr.columns.str.strip()
    hh.to_sql('households', conn, if_exists='replace', index=False)
    tx.to_sql('transactions', conn, if_exists='replace', index=False)
    pr.to_sql('products', conn, if_exists='replace', index=False)
    conn.close()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u == 'admin' and p == 'password123':
            session['user'] = u
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Wrong credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/data-pull', methods=['GET','POST'])
def data_pull():
    if 'user' not in session:
        return redirect(url_for('login'))
    rows = []
    hshd_num = '10'
    if request.method == 'POST':
        hshd_num = request.form['hshd_num']
    conn = sqlite3.connect('retail.db')
    query = """
        SELECT t.HSHD_NUM, t.BASKET_NUM, t.PURCHASE_,
               t.PRODUCT_NUM, p.DEPARTMENT, p.COMMODITY,
               t.SPEND, t.UNITS, t.STORE_R, t.WEEK_NUM, t.YEAR
        FROM transactions t
        LEFT JOIN products p ON t.PRODUCT_NUM = p.PRODUCT_NUM
        LEFT JOIN households h ON t.HSHD_NUM = h.HSHD_NUM
        WHERE t.HSHD_NUM = ?
        ORDER BY t.HSHD_NUM, t.BASKET_NUM, t.PURCHASE_,
                 t.PRODUCT_NUM, p.DEPARTMENT, p.COMMODITY
    """
    rows = conn.execute(query, (hshd_num,)).fetchall()
    conn.close()
    return render_template('data_pull.html', rows=rows, hshd_num=hshd_num)

@app.route('/load-data', methods=['GET','POST'])
def load_data_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    msg = ''
    if request.method == 'POST':
        load_data()
        msg = 'Data loaded successfully!'
    return render_template('load_data.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
    if os.path.exists('400_households.csv'):
        load_data()
    app.run(debug=True)
