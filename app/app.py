import os
import random
import string
import logging
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import psycopg2
import requests

# ---- Log ayarları ----
LOG_FILE = "/logs/activity.log"   # docker-compose ile bağlanan klasör
os.makedirs("/logs", exist_ok=True)

logger = logging.getLogger("project_app")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s | USER=%(user)s | ACTION=%(action)s | TARGET=%(target)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ContextAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        context = {
            "user": kwargs.pop("user", "-"),
            "action": kwargs.pop("action", "-"),
            "target": kwargs.pop("target", "-"),
        }
        kwargs["extra"] = context
        return msg, kwargs

log = ContextAdapter(logger, {})

# ---- Flask ----
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

# ---- DB bağlantısı ----
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "sifre123")
    )

# ---- Kullanıcılar ----
USERS = {
    "admin":   {"password": "admin123",   "role": "admin"},
    "adder":   {"password": "adder123",   "role": "adder"},
    "editor":  {"password": "editor123",  "role": "editor"},
    "deleter": {"password": "deleter123", "role": "deleter"},
    "viewer":  {"password": "viewer123",  "role": "viewer"},
}

# ---- Yardımcı: random string ----
def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ---- Login ----
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = USERS.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]

            log.info("Login başarılı", user=username, action="LOGIN", target="-")

            return redirect(url_for("index"))
        else:
            error = "Kullanıcı adı veya şifre hatalı."

    return render_template("login.html", error=error)

# ---- Logout ----
@app.route("/logout")
def logout():
    if "username" in session:
        log.info("Çıkış yapıldı", user=session["username"], action="LOGOUT", target="-")
    session.clear()
    return redirect(url_for("login"))

# ---- Ana sayfa ----
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    username = session.get("username")
    message = ""

    if request.method == "POST":
        user_id = request.form.get("user_id") or None
        name = request.form.get("name")
        email = request.form.get("email")
        uname = request.form.get("username") or random_string()
        password = request.form.get("password") or random_string()

        conn = get_connection()
        cur = conn.cursor()

        if user_id:
            if role not in ("admin", "editor"):
                message = "Bu işlem için yetkiniz yok (güncelleme)."
            else:
                cur.execute(
                    "UPDATE users SET name=%s, email=%s, username=%s, password=%s WHERE id=%s",
                    (name, email, uname, password, user_id)
                )
                conn.commit()
                log.info("Kullanıcı güncellendi", user=username, action="UPDATE", target=user_id)
                message = "Kullanıcı güncellendi."
        else:
            if role not in ("admin", "adder"):
                message = "Bu işlem için yetkiniz yok (ekleme)."
            else:
                cur.execute(
                    "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
                    (name, email, uname, password)
                )
                conn.commit()
                log.info("Kullanıcı eklendi", user=username, action="ADD", target=uname)
                message = f"Kullanıcı eklendi. Username: {uname}, Password: {password}"

        cur.close()
        conn.close()

    # Listeleme
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, username FROM users ORDER BY id")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", users=users, message=message)

# ---- Silme ----
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "username" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    username = session.get("username")
    if role not in ("admin", "deleter"):
        return "Bu işlem için yetkiniz yok (silme).", 403

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    log.info("Kullanıcı silindi", user=username, action="DELETE", target=user_id)

    return redirect(url_for("index"))

# ---- Rastgele kullanıcı ekleme (API) ----
@app.route("/add_random_user", methods=["GET"])
def add_random_user():
    if "username" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    username = session.get("username")
    if role not in ("admin", "adder"):
        return "Bu işlem için yetkiniz yok (API üzerinden ekleme).", 403

    resp = requests.get("https://randomuser.me/api/")
    if resp.status_code != 200:
        return jsonify({"error": "API'den veri alınamadı"}), 500

    data = resp.json()
    user_info = data["results"][0]["name"]
    full_name = f"{user_info['first']} {user_info['last']}"
    email = data["results"][0]["email"]
    uname = random_string()
    password = random_string()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
        (full_name, email, uname, password)
    )
    conn.commit()
    cur.close()
    conn.close()

    log.info("Kullanıcı eklendi", user=username, action="ADD", target=uname)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

