import psycopg2
import requests
from flask import Flask, render_template, request, redirect

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="root",
                        host="localhost",
                        port="5432")

app = Flask(__name__)
app.debug = True

cursor = conn.cursor()

@app.route('/')
def empty():
    return redirect('/login/')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')

            if len(username) == 0 or len(password) == 0:
                return render_template('error.html', err_text='Заполните логин или пароль')
            cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 0:
                return render_template('error.html', err_text='Пользователь не найден')
            else:
                return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if '1' in name or '2' in name or '3' in name or '4' in name or '5' in name or '6' in name or '7' in name or '8' in name or '9' in name or '0' in name  :
            return render_template('error.html', err_text='Имя пользователя не может содержать цифры')
        if len(name) == 0 or len(login) == 0 or len(password) == 0:
            return render_template('error.html', err_text='Пустые поля недопустимы')
        cursor.execute("SELECT login FROM users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) != 0:
            return render_template('error.html', err_text='Имя ' + str(login) + ' занято')
        else:
            cursor.execute('INSERT INTO users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)