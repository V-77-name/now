from flask import Flask, render_template, request, redirect
import pymysql
import os

app = Flask(__name__)

# Railway MySQL config (uses environment variables)
DB_HOST = os.getenv("MYSQLHOST", "localhost")
DB_USER = os.getenv("MYSQLUSER", "root")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "")
DB_NAME = os.getenv("MYSQLDATABASE", "portfolio")

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    with connection.cursor() as cursor:
        sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        connection.commit()

    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)