from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "devkey123"

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
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

init_db()

messages = []

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return redirect("/chat")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# LOGIN (INTENTIONALLY VULNERABLE)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # ⚠️ INTENTIONALLY VULNERABLE
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        print(query)

        c.execute(query)

        user = c.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/chat")

    return render_template("login.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        msg = request.form["message"]
        messages.append((session["user"], msg))

    return render_template("chat.html", messages=messages, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
