import os
import smtplib
from flask import Flask, send_from_directory, redirect, url_for, session, render_template, request, abort, jsonify
import databes_check as dc

app = Flask(__name__)
app.secret_key = "that´s_a_really_good,_long_and_secret_secret_key!1234"

allowed_urls = ("index.html", "verschiedenes/impressum.html", "verschiedenes/datenschutz.html", "verschiedenes"
                                                                                                "/kontakt.html",
                "verschiedenes/kontaktIframe.html", "register")


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.errorhandler(404)
def errorhandler404(e):
    return redirect("/index.html")


@app.errorhandler(403)
def errorhandler403(e):
    return f"<center><h1>Du hast keine Berechtigung um diesen Befehl auszuführen</h1><a href={redirect('/index.html')} zurück" \
           f"</a></center> "


def authorized(mode="checksession", **kwargs):
    if mode == "checksession":
        if "name" and "password" in session:
            if dc.checkUser(session["name"], session["password"]):
                print("login erkannt")
                return True
            else:
                return False
        else:
            try:
                if dc.checkUser(kwargs["name"], kwargs["password"]):
                    session["name"] = kwargs["name"]
                    session["password"] = kwargs["password"]
                    return True
            except:
                pass
        print("unauthorized")
        return False
    raise RuntimeError


# ==================================================================================================================== #
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if not authorized(name=request.form.get("name"), password=request.form.get("password")):
            return redirect(url_for("login"))
    return redirect("/index.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if "name" in session:
        session.pop("name", None)
        session.pop("password", None)
    return render_template("login.html")


@app.route("/adminpanel", methods=["POST", "GET"])
def adminpanel():
    if not authorized():
        return redirect(url_for("login"))
    rang = dc.return_values(value="rang", user=session["name"])
    # logging.info(session["name"] + " access to admin panel")
    if rang >= 2:
        # logging.warning(session["name"] + " tried to access to admin panel")
        abort(403)  # kick users without permissions

    if request.method == "GET":
        try:
            if request.args.get("t") is not None:
                user_form = request.args.get("t")
                if "~" in user_form:
                    user_form = user_form.split("~")
                else:
                    list(user_form).append("NoneObj")
                if user_form[0] == "del":
                    if user_form[1] != "Tobias":
                        dc.delete_user(user_form[1])
                        if user_form[1] == session["name"]:
                            return redirect(url_for("login"))
                    else:
                        #     logging.error(f"Access denied when {session['name']} tried to delete {user_form[1]}!")
                        # logging.info(f"{session['name']} delete {user_form[1]}")
                        pass

                elif user_form[0] == "change_password":
                    if session["name"] != "Tobias" and user_form[1] == "Tobias":
                        # logging.error(
                        #     f"Access denied when {session['name']} tried to change the password from {user_form[1]}!")
                        pass
                    else:
                        new_passwort = request.args.get("q")
                        dc.change_value(user_form[1], "change_password", new_passwort)  # change_password
                        # logging.info(f"{session['name']} changed the password from {user_form[1]}")
                        pass

                elif request.args.get("t") == "new_user":
                    neuer_nuter = request.args.get("tt")
                    passwort_form = request.args.get("s")
                    rang_form = request.args.get("gt")
                    dc.add_user(neuer_nuter, passwort_form, session["name"], rang_form)
                    # logging.info(f"{session['name']} created {neuer_nuter} with rang ({rang_form})")
                    pass
                else:
                    # logging.warning("Invalid Get-Method on Adminpanel:", user_form)
                    pass
                return redirect(url_for("adminpanel"))
        except AttributeError:
            pass

    userlist = dc.return_values(all=True)
    return render_template("adminpanel.html", len=len(userlist), userlist=userlist, rang=rang)


@app.route("/commit", methods=["POST", "GET"])
def commit():
    if not authorized():
        return redirect(url_for("login"))
    if request.method == "POST":
        # return list(request.form)[0]
        command = list(request.form)[0].split("~")
        # logging.info("Please Commit: ", command)
        if command[0] == "change_password":
            return render_template("change_user_password.html", name=list(request.form)[0].split("~")[1])
        elif command[0] == "del":
            return render_template("delete_user.html", name=list(request.form)[0].split("~")[1])
        elif command[0] == "newUser":
            return render_template("new_user.html")
    else:
        return "Ungültiger Post-Befehl"


@app.route("/register", methods=["POST", "GET"])
def register():
    print("Register")
    if request.method == "POST":
        print("Register post")
        username = request.json['username']
        password = request.json['password']
        register_try = dc.add_user(username, password, "SYSTEM", 2)
        print("LOLOL:")
        print(register_try)
        if register_try:
            response = {'message': 'Erfolgreich registriert!'}
            return jsonify(response), 200
        else:
            response = {'message': "User already registered"}
            return jsonify(response), 400

    print("ho")
    return render_template("register_user.html")


@app.route("/kontakt", methods=["POST"])
def handle_konakt():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Send email
    sender_email = 'balu.safemail@gmail.com'  # replace with your email address
    sender_password = 'ndlskbqublgjggym'  # replace with your email password

    receiver_email = 'balu.safemail@gmail.com'  # replace with the recipient email address

    smtp_server = 'smtp.gmail.com'  # replace with your SMTP server
    smtp_port = 587  # replace with the SMTP server port

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        print("Server started")
        server.login(sender_email, sender_password)
        print("login")
        email_message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage: {message}"
        print(email_message)
        server.sendmail(sender_email, receiver_email, email_message)
        print("done")
    return jsonify({'message': 'Message sent successfully!'})


@app.route('/<path:path>')
def serve_file(path):
    print(path)
    if path in allowed_urls:
        if path == "index.html":
            print("CORRECT")
            if authorized():
                if dc.return_values(value="rang", user=session["name"]) <= 1:
                    return render_template("index.html",
                                           loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a><br><a href=/adminpanel id=adminLink>Nutzerverwaltung</a></div>")
                return render_template("index.html",
                                       loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a></div>")
            return render_template("index.html", loginVar="<a href=\"/login\" id=loginLink>Login</a>")
        if authorized():
            if dc.return_values(value="rang", user=session["name"]) <= 1:
                return render_template(path,
                                       loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a><br><a href=/adminpanel id=adminLink>Nutzerverwaltung</a></div>")
            return render_template(path,
                                   loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a></div>"
                                   )
        return render_template(path, loginVar="<a href=\"/login\" id=loginLink>Login</a>")
    if not authorized():
        print("DISALLOWED: ")
        print(path)
        return redirect(url_for("login"))
    if ".css" in path or ".js" in path or ".png" in path or ".js" in path or ".jpg" in path:
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        return send_from_directory(directory, filename)
    if dc.return_values(value="rang", user=session["name"]) <= 1:
        return render_template(path,
                               loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a><br><a href=/adminpanel id=adminLink>Nutzerverwaltung</a></div>")
    return render_template(path,
                           loginVar=f"<div>Willkommen {session['name']}<br> <a href=\"/login\" id=logoutLink>Logout</a></div>")


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0", threaded=True)
