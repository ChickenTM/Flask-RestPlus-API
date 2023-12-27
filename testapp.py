import werkzeug
from werkzeug.utils import cached_property

werkzeug.cached_property = cached_property

import flask
from flask.scaffold import _endpoint_from_view_func

flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

from flask import Flask, abort
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound, HTTPException

app = Flask(__name__)
api = Api(app, validate=True)
app.config.SWAGGER_UI_JSONEDITOR = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdb.db"
app.config["ERROR_404_HELP"] = False


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    number = db.Column(db.String(10))


user_model = api.model(
    "User",
    {
        "id": fields.Integer,
        "name": fields.String("Name"),
        "number": fields.String("Number"),
    },
)


@api.errorhandler(NotFound)
def handle_404_error(error):
    return {
        "error": "no user with given ID found",
        "message": "Enter Correct data",
    }, 404


@api.errorhandler(HTTPException)
def handle_error(error):
    if error.code == 5:
        return {"message": error.description}, 5
    if error.code == 6:
        return {"message": error.description}, 6


@api.route("/users")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    @api.doc("getting the data")
    def get(self):
        if User.query.count() == 0:
            error = HTTPException()
            error.description = "DB is Empty"
            error.response = api.make_response({"message": error.description}, 5)
            raise error

            # raise HTTPException(description='No content', code=204)

        return User.query.all()

    @api.expect(user_model)
    def post(self):
        name = api.payload["name"]
        number = api.payload["number"]
        user = User(name=name, number=number)
        users = User.query.all()
        for U in users:
            if U.name == user.name and U.number == user.number:
                error = HTTPException()
                error.description = "User exists already"
                error.response = api.make_response({"message": error.description}, 6)
                raise error
        db.session.add(user)
        db.session.commit()
        return {"success": True}


@api.route("/users/<int:id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            raise NotFound
        return user

    @api.expect(user_model)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            raise NotFound
        user.name = api.payload["name"]
        user.number = api.payload["number"]
        db.session.commit()
        return {"success": True}

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            raise NotFound
        db.session.delete(user)
        db.session.commit()
        return {
            "Message": "This entry is deleted",
            "Data": "Name : {}, Number : {}".format(user.name, user.number),
        }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
