from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.secret_key = 'retail2024'

DB_URL = 'mssql+pyodbc://sqladmin:Starwars%402032@monukode-sqlsrv.database.windows.net/monukode-db?driver=ODBC+Driver+18+for+SQL+Server'

def get_engine():
    return create_engine(DB_URL)

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
    try:
        engine = get_engine()
        with engine.connect() as conn:
            query = text("""
                SELECT t."HSHD_NUM", t."BASKET_NUM", t."PURCHASE_",
                       t."PRODUCT_NUM", p."DEPARTMENT", p."COMMODITY",
                       t."SPEND", t."UNITS", t."STORE_R", t."WEEK_NUM", t."YEAR"
                FROM transactions t
                LEFT JOIN products p ON t."PRODUCT_NUM" = p."PRODUCT_NUM"
                WHERE t."HSHD_NUM" = :hshd_num
                ORDER BY t."HSHD_NUM", t."BASKET_NUM", t."PURCHASE_",
                         t."PRODUCT_NUM", p."DEPARTMENT", p."COMMODITY"
            """)
            result = conn.execute(query, {"hshd_num": int(hshd_num)})
            rows = result.fetchall()
    except Exception as e:
        print(e)
        rows = []
    return render_template('data_pull.html', rows=rows, hshd_num=hshd_num)

@app.route('/load-data', methods=['GET','POST'])
def load_data_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    msg = 'Data loaded in Supabase cloud database!'
    return render_template('load_data.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
