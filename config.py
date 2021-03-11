from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
try:
    from local_config import mongo_config, secret_key
except:
    mongo_config = {}
    secret_key = 'secret_xentric_!'

app = Flask(__name__)
app.secret_key = secret_key
default_datetime_format = '%Y-%m-%d %H:%M:%S'
app.config['JSON_AS_ASCII']         = False
app.config['MONGODB_DB']            = mongo_config.get('MONGODB_DB', 'xentric')
app.config['MONGODB_HOST']          = mongo_config.get('MONGODB_HOST', '127.0.0.1')
app.config['MONGODB_PORT']          = mongo_config.get('MONGODB_PORT', 27017)
app.config['MONGODB_USERNAME']      = mongo_config.get('MONGODB_USERNAME', None)
app.config['MONGODB_PASSWORD']      = mongo_config.get('MONGODB_PASSWORD', None)
app.config['MONGODB_AUTHSOURCE']    = mongo_config.get('MONGODB_AUTHSOURCE', None)
app.config['MONGODB_AUTHMECHANISM'] = mongo_config.get('MONGODB_AUTHMECHANISM', None)
app.config['MONGO_CONNECT']	    = mongo_config.get('MONGO_CONNECT', False)
db = MongoEngine(app)
