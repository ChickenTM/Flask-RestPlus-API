import werkzeug
from werkzeug.utils import cached_property
werkzeug.cached_property = cached_property

from werkzeug.wrappers.response import Response 
werkzeug.wrappers.BaseResponse = Response

#from werkzeug.routing import parse_rule as parse_rule
#werkzeug.routing.parse_rule = _parse_rule

import flask
from flask.scaffold import _endpoint_from_view_func
flask.helpers._endpoint_from_view_func = _endpoint_from_view_func

from flask import Flask
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, post_load

app = Flask(__name__)

api = Api(app)

app.config["SWAGGER_UI_JSONEDITOR"] = True

a_language = api.model('language', {'language' : fields.String('The Language'), 'framework' : fields.String('The framework')}) #, 'id' : fields.Integer('ID')})

class TheLanguage(object):
    def __init__(self, language, framework):
        self.language = language
        self.framework = framework
    
    def __repr__(self):
        return "{} is the language. {} is the framework.".format(self.language, self.framework)

class LanguageSchema(Schema):
    language = ma_fields.String()
    framework = ma_fields.String()

    @post_load
    def create_language(self, data, **kwargs):
        print(data)                 #left debugging here on friday, figure out why many -> unexpected kwarg
        return TheLanguage('python','django')


languages = []
#python = {"language" : "python", "id" : 1}
python = TheLanguage(language = 'Python', framework = 'Flask')
languages.append(python)

@api.route('/language')
class Language(Resource):

    #@api.marshal_with(a_language, envelope = 'the_data')
    def get(self):
        schemas = LanguageSchema(many=True) 
        return schemas.dump(languages)

    @api.expect(a_language)
    def post(self):
        schema = LanguageSchema(many=False)
        new_language = schema.load(api.payload)
      
        #new_langauge['id'] = len(languages) + 1
        languages.append(new_language)
        return {'result' : 'language added'}, 201


if __name__ == '__main__':
    app.run(debug=True)

