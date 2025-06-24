from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC")
    alerts = cursor.fetchall()
    return render_template('dashboard.html', alerts=alerts)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
