from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "devkey123"

messages = []

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return redirect("/chat")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
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
