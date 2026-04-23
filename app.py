from flask import Flask, render_template, request, redirect, flash, jsonify
from services.auth_service import login_user, register_user
#from application.routes.map_routes import map_bp

from application.services.adaptive_generator_ml import generate_adaptive_map_ml

app = Flask(__name__)
app.secret_key = "rhizome-secret-key"

# Registrar blueprint existente
#app.register_blueprint(map_bp, url_prefix="/api")


# -----------------------
# VISTAS
# -----------------------

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -----------------------
# AUTH
# -----------------------

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


# -----------------------
# NUEVO ENDPOINT ADAPTATIVO
# -----------------------

@app.route("/api/generate-adaptive", methods=["POST"])
def generate_adaptive():
    try:
        data = request.json

        config = {
            "ancho": data.get("ancho", 30),
            "alto": data.get("alto", 20),
            "probabilidad": data.get("probabilidad", 0.45),
            "iteraciones": data.get("iteraciones", 4),
            "seed": data.get("seed", None)
        }

        user_profile = data.get("user_profile", {})
        user_behavior = data.get("user_behavior", {})
        context = data.get("context", {})

        resultado = generate_adaptive_map_ml(
            config,
            user_profile,
            user_behavior,
            context
        )

        return jsonify({
            "status": "success",
            "score": resultado["score"],
            "config_final": resultado["config_final"],
            "metricas": resultado["metricas"],
            "map": resultado["map"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -----------------------
# RUN
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)