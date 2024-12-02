from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Создание базы данных
def init_db():
    with sqlite3.connect("requests.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                problem TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        conn.commit()

# Главная страница для просмотра заявок
@app.route("/")
def home():
    with sqlite3.connect("requests.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests ORDER BY timestamp DESC")
        requests = cursor.fetchall()
    return render_template("admin.html", requests=requests)

# Обработка заявки с основного сайта
@app.route("/send", methods=["POST"])
def send_request():
    problem = request.form["problem"]
    phone = request.form["phone"]
    address = request.form["address"]
    with sqlite3.connect("requests.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (problem, phone, address) VALUES (?, ?, ?)",
                       (problem, phone, address))
        conn.commit()
    return "Заявка отправлена! Мы свяжемся с вами.", 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
