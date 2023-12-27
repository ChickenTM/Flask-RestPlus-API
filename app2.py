'''import werkzeug
from werkzeug.utils import cached_property
werkzeug.cached_property = cached_property

import flask
from flask.scaffold import _endpoint_from_view_func
flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

from werkzeug.wrappers.response import Response 
werkzeug.wrappers.BaseResponse = Response'''

from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)


a_language = api.model('Language', {'language' : fields.String('The Language'), 'id' : fields.Integer("ID")})

languages = []
python = {'language' : 'python', 'id' : 1} 
languages.append(python)

@api.route('/language')
class language(Resource):
    
    @api.marshal_with(a_language, envelope="data")
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        new_language = api.payload
        new_language['id'] = len(languages) + 1
        languages.append(api.payload)
        return {'result' : 'Language added'}, 201 

    def delete(self):
        pass

    def put(self):
        pass






if __name__ == '__main__':
    app.run(debug=True)
