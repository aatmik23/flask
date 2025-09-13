from flask import Flask, request, Response, url_for, session, redirect

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"DEBUG: username={username}, password={password}")  # Print to console

        if username == "admin" and password == "123":
            session["user"] = username
            return redirect(url_for("welcome"))
        else:
            return Response("Invalid ID or password", mimetype="text/plain")
    else:
        return '''
            <h2>Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Login">
            </form>
        '''

@app.route("/welcome")
def welcome():
    if "user" in session:
        return f'''Welcome, {session["user"]}!
        <a href="{url_for("logou")}">logout</a>'''
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logou():

        session.pop("user", None)
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
