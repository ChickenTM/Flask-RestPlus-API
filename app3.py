import werkzeug
from werkzeug.utils import cached_property
werkzeug.cached_property = cached_property

import flask
from flask.scaffold import _endpoint_from_view_func
flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

from werkzeug.wrappers.response import Response 
werkzeug.wrappers.BaseResponse = Response

from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =  False

api = Api(app)

db = SQLAlchemy(app)

datamodel = api.model('data',{'name' : fields.String('Enter name')})

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.id


    @api.route('/data/')
    class database(Resource):
        def __init__(self,name):
            self.name = name

        def get(self):
            datas = Data.query.order_by(Data.id).all()
            return datas

        @api.expect(datamodel)
        def post(self):
            name = api.payload['name']
            datas = Data(name = name)
            db.session.add(datas)
            db.session.commit()

        
    
if __name__ == '__main__':
    app.run()