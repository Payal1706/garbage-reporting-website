from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# =========================
# Upload Configuration
# =========================
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# Database Connection
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Payalkhuntia@17",
        database="garbage_db"
    )

# =========================
# Home Page
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# Report Page
# =========================
@app.route("/report")
def report():
    return render_template("report.html")

# =========================
# Submit Complaint
# =========================
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    location = request.form["location"]
    garbage_type = request.form["garbage_type"]
    description = request.form["description"]

    photo = request.files["photo"]
    filename = ""

    if photo and photo.filename != "":
        original = secure_filename(photo.filename)
        filename = datetime.now().strftime("%Y%m%d%H%M%S_") + original
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO complaints 
        (name, location, garbage_type, description, photo, status)
        VALUES (%s,%s,%s,%s,%s,'Pending')
    """, (name, location, garbage_type, description, filename))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# =========================
# Status Page
# =========================
@app.route("/status", methods=["GET", "POST"])
def status():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    complaints = []
    searched = False

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        searched = True

        cur.execute("""
            SELECT * FROM complaints
            WHERE name LIKE %s AND location LIKE %s
            ORDER BY id DESC
        """, (f"%{name}%", f"%{location}%"))

        complaints = cur.fetchall()

    conn.close()

    return render_template("status.html", complaints=complaints, searched=searched)

# =========================
# Admin Panel
# =========================
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM complaints ORDER BY id DESC")
    data = cur.fetchall()

    conn.close()
    return render_template("admin.html", complaints=data)


    # =========================
# Contact Us Page
# =========================
@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# =========================
# Address Page
# =========================
@app.route("/address")
def address():
    return render_template("address.html")

# =========================
# Update Complaint Status
# =========================
@app.route("/update_status", methods=["POST"])
def update_status():
    cid = request.form["id"]
    new_status = request.form["status"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE complaints SET status=%s WHERE id=%s", (new_status, cid))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True)
