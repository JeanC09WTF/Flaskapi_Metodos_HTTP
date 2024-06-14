
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prueba.db'
db = SQLAlchemy (app)

#crea el modelo en la base de datos

class Prueba1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    
    def serialize(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone
        }
    

# Crea las tablas en la base de datos
with app.app_context():
    db.create_all()


# Creando rutas

@app.route('/prueba', methods = ['GET','POST'])
def get_prueba():
    if request.method == 'POST':
        data = request.get_json()
        Prueba2 = Prueba1(name = data['name'], email = data['email'], phone = data['phone'])
        db.session.add(Prueba2)
        db.session.commit()
        return jsonify({'message':'Contacto creado', 'prueba2': Prueba2.serialize()}), 201
    elif request.method == 'GET':
        prueba = Prueba1.query.all()
        return jsonify([prue.serialize() for prue in prueba])
        

@app.route('/prueba/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_prueba_by_id(id):
    prueba = Prueba1.query.get(id)
    if not prueba:
        return jsonify({'message': 'Contacto no encontrado'}), 404
    
    if request.method == 'DELETE':
        db.session.delete(prueba)
        db.session.commit()
        return jsonify({'message': 'Contacto eliminado'})

    if request.method == 'PUT':
        data = request.get_json()
        prueba.name = data.get('name', prueba.name)
        prueba.email = data.get('email', prueba.email)
        prueba.phone = data.get('phone', prueba.phone)
        db.session.commit()
        return jsonify({'message': 'Contacto actualizado', 'prueba': prueba.serialize()})
    
    return jsonify(prueba.serialize())


# @app.route('/')
# def home():
#     return jsonify({"mensaje": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)


