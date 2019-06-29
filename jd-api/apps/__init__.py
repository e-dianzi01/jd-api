from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app,supports_credentials=True )

# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
#
# app.after_request(after_request)
# cors = CORS(app, resources={r"//*": {"origins": "*"}})
