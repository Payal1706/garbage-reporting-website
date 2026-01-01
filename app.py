from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- Database Connection ----------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Home Page ----------
@app.route('/')
def home():
    return render_template('index.html')


# ---------- Report Page ----------
@app.route('/report')
def report():
    return render_template('report.html')


# ---------- Submit Form ----------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mobile = request.form['mobile']
    location = request.form['location']
    garbage_type = request.form['garbage_type']
    description = request.form['description']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports (name, mobile, location, garbage_type, description)
        VALUES (?, ?, ?, ?, ?)
    """, (name, mobile, location, garbage_type, description))

    conn.commit()
    conn.close()

    return redirect('/admin')


# ---------- Admin Panel ----------
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", data=data)


# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True)
