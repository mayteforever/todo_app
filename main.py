from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motos.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class MarcaMoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_origen = db.Column(db.String(100), nullable=False)
    fundacion = db.Column(db.Integer, nullable=False)
    confirmacion = db.Column(db.String(3), nullable=False, default= "No")  # Campo de confirmación

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    marcas = MarcaMoto.query.all()
    return render_template('index.html', marcas=marcas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    pais_origen = request.form.get('pais_origen')
    fundacion = request.form.get('fundacion')

    nueva_marca = MarcaMoto(nombre=nombre, pais_origen=pais_origen, fundacion=fundacion)
    db.session.add(nueva_marca)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    marca = MarcaMoto.query.get(id)
    if marca:
        db.session.delete(marca)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/confirmar/<int:id>', methods=['POST'])
def confirmar(id):
    marca = MarcaMoto.query.get(id)
    if marca:
        # Alternar entre "Sí" y "No"
        marca.confirmacion = "No" if marca.confirmacion == "Sí" else "Sí"
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
