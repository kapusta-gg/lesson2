from flask import jsonify
from flask_restful import abort, Resource
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User
from data.users_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        return jsonify({'user': user.to_dict(
            only=("name", "surname", "age", "position", "speciality", "address", "email"))})

    def delete(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(only=("name", "surname", "age", "position",
                                                    "speciality", "address", "email")) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            address=args['address'],
            email=args['email'],
            position=args['position'],
            speciality=args['speciality'],
            hashed_password=generate_password_hash(args['hashed_password'])
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


