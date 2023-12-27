import werkzeug
from werkzeug.utils import cached_property
werkzeug.cached_property = cached_property

#import flask
#from flask.scaffold import _endpoint_from_view_func
#flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.SWAGGER_UI_JSONEDITOR = True

db = SQLAlchemy(app)

student_model = api.model('Student', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True),
    'age': fields.Integer(required=True),
    'course': fields.String(required=True)
})
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

@api.route('/students/<int:id>')
class StudentResource(Resource):
    @api.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        if student:
            return student
        api.abort(404, "Student {} doesn't exist".format(id))
    
    @api.marshal_with(student_model)
    @api.expect(student_model)
    def put(self, id):
        student = Student.query.get(id)
        if student:
            student.name = api.payload['name']
            student.age = api.payload['age']
            student.course = api.payload['course']
            db.session.commit()
            return student
        api.abort(404, "Student {} doesn't exist".format(id))
    def delete(self, id):
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {"message": "Student {} has been deleted".format(id)}
        api.abort(404, "Student {} doesn't exist".format(id))
@api.route('/students')
class StudentListResource(Resource):
    @api.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
    @api.marshal_with(student_model)
    @api.expect(student_model)
    def post(self):
        student = Student(api.payload['name'], api.payload['age'], api.payload['course'])
        db.session.add(student)
        db.session.commit()
        return student, 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)