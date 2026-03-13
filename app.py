from flask import Flask, render_template, request, redirect, flash
from services.auth_service   import login_user, register_user

app = Flask(__name__)

app.secret_key = "rhizome-secret-key"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    try:

        res = login_user(email, password)

        if res.user:
            flash("Bienvenido a Rhizome", "success")
            return redirect("/dashboard")

        else:
            flash("Correo o contraseña incorrectos", "error")
            return redirect("/")

    except Exception as e:

        error = str(e)

        if "Invalid login credentials" in error:
            flash("Credenciales incorrectas", "error")

        else:
            flash("Error del servidor", "error")

        return redirect("/")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():

    email = request.form["email"]
    password = request.form["password"]

    res = register_user(email, password)

    if res and res.user:
        flash("Cuenta creada correctamente. Ahora puedes iniciar sesión.", "success")
        return redirect("/")
    else:
        flash("Error al crear usuario", "error")
        return redirect("/register-page")

if __name__ == "__main__":
    app.run(debug=True)