# app.py
import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from database import init_db_pool
import models

app = Flask(__name__)

# Inicializar pool
init_db_pool()

@app.route("/")
def index():
    return render_template("index.html")

# JSON endpoints (útiles para JMeter/Postman)
@app.route("/api/productos", methods=["GET"])
def api_productos():
    prods = models.list_products()
    return jsonify(prods), 200

@app.route("/api/productos/<int:pid>", methods=["GET"])
def api_producto(pid):
    prod = models.get_product(pid)
    if not prod:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(prod), 200

@app.route("/api/comprar", methods=["POST"])
def api_comprar():
    data = request.get_json() or {}
    pid = data.get("producto_id")
    qty = int(data.get("cantidad", 1))
    if not pid:
        return jsonify({"status":"ERROR","mensaje":"producto_id requerido"}), 400
    success, info = models.purchase_product(pid, qty)
    if success:
        return jsonify({"status":"OK", **info}), 201
    else:
        return jsonify({"status":"ERROR","mensaje": info}), 400

# Rutas simples con HTML para demostración
@app.route("/productos")
def view_productos():
    prods = models.list_products()
    return render_template("productos.html", productos=prods)

@app.route("/comprar", methods=["GET","POST"])
def view_comprar():
    if request.method == "GET":
        prods = models.list_products()
        return render_template("comprar.html", productos=prods, result=None)
    # POST
    pid = int(request.form.get("producto_id"))
    qty = int(request.form.get("cantidad", 1))
    success, info = models.purchase_product(pid, qty)
    if success:
        return render_template("comprar.html", productos=models.list_products(), result=("OK", info))
    else:
        return render_template("comprar.html", productos=models.list_products(), result=("ERROR", info))

if __name__ == "__main__":
    # puerto 5000 por defecto
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
