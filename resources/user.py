import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModels


class UserRegister(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    parse.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    def post(self):
        data = UserRegister.parse.parse_args()

        if UserModels.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModels(**data)
        user.save_user()

        return {'message': 'User register successfully'}, 201