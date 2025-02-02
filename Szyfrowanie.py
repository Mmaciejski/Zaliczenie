from flask import Flask, request, render_template_string
import sqlite3
import base64
from Crypto.Cipher import AES
import os

app = Flask(__name__)
SECRET_KEY = b'Sixteen byte key'

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_message(enc_message, key):
    enc_data = base64.b64decode(enc_message)
    nonce = enc_data[:16]
    ciphertext = enc_data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template_string('''
        <h2>Aplikacja z szyfrowaniem AES i podatnością na SQL Injection</h2>
        <form action="/encrypt" method="post">
            <input type="text" name="message" placeholder="Wiadomość do zaszyfrowania" required>
            <button type="submit">Szyfruj</button>
        </form>
        <form action="/decrypt" method="post">
            <input type="text" name="enc_message" placeholder="Zaszyfrowana wiadomość" required>
            <button type="submit">Deszyfruj</button>
        </form>
        <h3>SQL Injection</h3>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Nazwa użytkownika" required>
            <input type="password" name="password" placeholder="Hasło" required>
            <button type="submit">Zaloguj</button>
        </form>
        <h3>Bezpieczne logowanie</h3>
        <form action="/secure_login" method="post">
            <input type="text" name="username" placeholder="Nazwa użytkownika" required>
            <input type="password" name="password" placeholder="Hasło" required>
            <button type="submit">Zaloguj</button>
        </form>
    ''')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form['message']
    enc_message = encrypt_message(message, SECRET_KEY)
    return f'Zaszyfrowana wiadomość: {enc_message}'

@app.route('/decrypt', methods=['POST'])
def decrypt():
    enc_message = request.form['enc_message']
    try:
        dec_message = decrypt_message(enc_message, SECRET_KEY)
        return f'Odszyfrowana wiadomość: {dec_message}'
    except Exception as e:
        return f'Błąd podczas deszyfrowania: {str(e)}'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Niebezpieczna podatność SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()
    if user:
        return 'Zalogowano pomyślnie!'
    return 'Błędne dane logowania!'

@app.route('/secure_login', methods=['POST'])
def secure_login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Zabezpieczona wersja logowania - użycie parametrów
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return 'Zalogowano pomyślnie (bezpieczna wersja)!'
    return 'Błędne dane logowania!'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
