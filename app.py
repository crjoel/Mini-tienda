from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'clave-secreta'

productos = [
    {"id": 1, "nombre": "Camisa", "precio": 10, "imagen": "descargar.jpeg"},
    {"id": 2, "nombre": "Pantalón", "precio": 50, "imagen": "pantalon.jpeg"},
    {"id": 3, "nombre": "Zapatos", "precio": 80, "imagen": "zapatos.jpeg"},
]

@app.route('/')
def index():
    carrito = session.get('carrito', [])
    cantidad = len(carrito)
    return render_template("index.html", productos=productos, cantidad=cantidad)

@app.route('/agregar/<int:producto_id>')
def agregar(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(producto_id)
    session.modified = True
    flash("Producto agregado al carrito.")
    return redirect(url_for('index'))

@app.route('/eliminar/<int:index>')
def eliminar(index):
    if 'carrito' in session and index < len(session['carrito']):
        session['carrito'].pop(index)
        session.modified = True
        flash("Producto eliminado del carrito.")
    return redirect(url_for('carrito'))

@app.route('/carrito')
def carrito():
    items = []
    total = 0
    carrito_ids = session.get('carrito', [])
    for id in carrito_ids:
        producto = next((p for p in productos if p['id'] == id), None)
        if producto:
            items.append(producto)
            total += producto['precio']
    return render_template("cart.html", items=items, total=total, cantidad=len(carrito_ids))

if __name__ == '__main__':
    app.run(debug=True)


