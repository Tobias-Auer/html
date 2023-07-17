# import logging

from flask import Flask, render_template, request, url_for, redirect, session, abort

import databes_check as dc

# logfile = "log.txt"

# logging.basicConfig(filename=logfile,
#                     filemode='a',
#                     format=f'%(levelname)s: %(asctime)s {"-"*5}%(name)s{"-"*10+">"}%(message)s\n{"#"*50}',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
#
# logging.getLogger('werkzeug').disabled = True
app = Flask(__name__)
app.secret_key = "that´s_a_really_good,_long_and_secret_secret_key!1234"


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.errorhandler(404)
def errorhandler404(e):
    return redirect(url_for("index"))


@app.errorhandler(403)
def errorhandler403(e):
    return f"<center><h1>Du hast keine Berechtigung um diesen Befehl auszuführen</h1><a href={redirect('/')} zurück" \
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


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if not authorized(name=request.form.get("name"), password=request.form.get("password")):
            return redirect(url_for("login"))
        return redirect(request.url)
    else:
        if not authorized():
            return redirect(url_for("login"))

    name = session["name"]
    rang = dc.return_values(value="rang", user=name)
    return render_template("index.html", name=name, rang=rang)


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


if __name__ == '__main__':
    # logging.info("\tStarting server...")
    # os.system("ipconfig")
    app.run(port=80, host="0.0.0.0", debug=True, threaded=True)
