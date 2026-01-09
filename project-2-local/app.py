from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_CONFIG = {
    'dbname': 'proje2_db',
    'host': 'localhost',
    'port': '5432'
}

# PostgreSQL bağlantısı
def get_db_connection(username, password):
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=username,
            password=password,
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print("Bağlantı hatası:", e)
        return None

def get_session_connection():
    if "username" in session and "password" in session:
        return get_db_connection(session["username"], session["password"])
    return None

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection(username, password)
        if conn:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('index'))
        else:
            return "Giriş başarısız! Kullanıcı adı veya şifre hatalı."
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Anasayfa
@app.route('/')
def index():
    conn = get_session_connection()
    if not conn:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)

# Kullanıcı ekleme
@app.route('/add', methods=['POST'])
def add_user():
    conn = get_session_connection()
    if not conn:
        return redirect(url_for('login'))

    name = request.form.get('name')
    email = request.form.get('email')

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
    except Exception as e:
        return f"Hata: {e}"
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

# Kullanıcı silme
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = get_session_connection()
    if not conn:
        return redirect(url_for('login'))

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        return f"Hata: {e}"
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

# Kullanıcı düzenleme
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_session_connection()
    if not conn:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        try:
            cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s",
                           (name, email, user_id))
            conn.commit()
        except Exception as e:
            return f"Hata: {e}"
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

