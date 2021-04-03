import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList



app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#   LEVANTA LAS EXCEPCIONES PROPIAS, CODIGO Y MENSAJES DEL ERROR ESPECIFICO
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key ='jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#	 VINCULANDO EL JWT CON LA APP
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):    #   FUNCION PARA AGREGAR DATOS EXTRA EN LA RESPUESTA DEL TOKEN
    if identity == 1:   # El "1" es el ID del usuario que se creo con la BD sqlite
        return {'is_admin': True}
    return {'is_admin': False}

#	AGREGANDO EL RECURSO "STUDENT" 
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/user/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

#	SOLO SE VA EJECUTAR EL ARCHIVO app.py
if __name__ == '__main__':

    db.init_app(app)
    app.run(port=5000, debug=True)