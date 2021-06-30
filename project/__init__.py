from flask import Flask, request, jsonify, render_template, make_response
import jwt
import re
from project.config.config import *
from functools import wraps
import json
from flask_cors import CORS, cross_origin


app = Flask('project')
app.config['SECRET_KEY'] = "Sagar@1997"
app.config['custom_config']  = conf
tokendata = {}
def token_authenticator(expected_role=""):
    def inner_decorator(fun):
        @wraps(fun) 
        def inner1(*args, **kwargs):
            try:
                authorization = request.headers.get('authorization')
                if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    tokendata_local = json.loads(jwt.decode(token, app.config['SECRET_KEY'])['data'])
                    tokendata['id'] = tokendata_local['id']
                    tokendata['rolename'] = tokendata_local['rolename']
                    
                    if expected_role!="":
                        if tokendata_local['rolename'] in expected_role or expected_role==tokendata_local['rolename']:
                            return fun(*args, **kwargs)
                        else:
                            return make_response({"ERROR":"INVALID_ROLE"})
                    else:
                        return fun(*args, **kwargs)
                else:
                    return make_response({"ERROR":"INVALID_AUTHORIZATION_HEADER"}, 403)
            except Exception as e:
                print(e)
                return make_response({"ERROR":str(e), "FROM":"__init__.py"}, 403)
        return inner1
    return inner_decorator

from project.controllers import *