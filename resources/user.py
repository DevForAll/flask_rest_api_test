import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
    )
from models.user import UserModels
from blacklist import BLACKLIST


_user_parse = reqparse.RequestParser()
_user_parse.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank"
)

_user_parse.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank"
)

class UserRegister(Resource):
    def post(self):
        data = _user_parse.parse_args()

        if UserModels.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # user = UserModels(data['username'], data['password'])
        user = UserModels(**data)
        user.save_user()

        return {'message': 'User register successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModels.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModels.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        #   OBTENER DATOS PARA ANALIZAR
        data = _user_parse.parse_args()
        #   BUSCAR AL USUARIO EN BASE DE DATOS
        user = UserModels.find_by_username(data['username'])
        #   COMPROBAMOS LA EXISTENCIA DEL USER Y LA CONTRASEÑA
        #   esta es la funcion authenticate()
        if user and safe_str_cmp(user.password, data['password']):
            #   identity = 'esta es la funcion identity()'
            access_token = create_access_token(identity= user.id, fresh= True)
            #   CREANDO TOKEN DE ACTUALIZACION (refresh)
            refresh_token = create_refresh_token(user.id)
            #   RETORNAR
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] #   jti es "JWT ID", un identificador unico para un JWT
        BLACKLIST.add(jti)
        return {'message': 'Se desconectó correctamente'}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True) #   CON ESTE DECORADOR SE VA RECIBIR UN TOKEN DE ACTUALIZACION
    def post(self):
        current_user = get_jwt_identity()   #Obteniendo la identidad del usuario
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token,}, 200
