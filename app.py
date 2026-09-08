from flask import Flask, render_template, request
import psycopg2
from dotenv import load_dotenv
import os
import gunicorn

app = Flask(__name__)

load_dotenv()

try:
    connection = psycopg2.connect(
        host='localhost',
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        port=os.getenv('PORT')
    )


    cursor = connection.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS todo_list(
        id SERIAL PRIMARY KEY,
        task VARCHAR(30),
        status VARCHAR(10)
    );
    """

    cursor.execute(sql)
    connection.commit()
    print("Database connected successfully")

except Exception as e:
    print("DB connection error:", e)


@app.route('/', methods=['POST'])
def home():
    data = request.json
    input_value = data['input']
    status = data['status']

    query = """INSERT INTO todo_list (task, status) VALUES (%s, %s)"""
    cursor.execute(query, (input_value, status,))
    connection.commit()

    query = """SELECT COUNT(*) FROM todo_list"""
    cursor.execute(query)
    connection.commit()

    res = cursor.fetchone()

    return str(res[0])


@app.route('/done', methods=['POST'])
def complete():
    data = request.json
    value = data['task']
    status = data['status']

    query = """UPDATE todo_list SET status = %s WHERE task = %s"""
    cursor.execute(query, (status, value,))
    connection.commit()

    return ''


@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    value = data['task']

    query = """DELETE FROM todo_list WHERE task = %s"""
    cursor.execute(query, (value,))
    connection.commit()

    query = """SELECT COUNT(*) FROM todo_list"""
    cursor.execute(query)
    connection.commit()

    res = cursor.fetchone()

    return str(res[0])


@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)