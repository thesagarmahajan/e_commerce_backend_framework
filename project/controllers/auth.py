# Important Imports
from imports import *

# Importing Model (Business Login)
from project.models.auth_model import auth_model
# Initializing Obejct of imported model class
authobj = auth_model()

# Password Based
@app.route('/auth/<role>/password_based', methods=['POST'])
@cross_origin()
def password_based(role):
    try:
        uname = request.form['email']
        pwd = request.form['password']
        return make_response(jsonify({"data":authobj.password_based(role, uname, pwd)}), 200)
    except Exception as e:
        raise e
        return make_response(jsonify({"ERROR":"INVALID_KEY_VALUE"}))
    
@app.route('/auth/signin', methods=['POST'])
@token_authenticator("admin")
def signin():
    try:
        data = {
            "full_name": request.form['full_name'],
            "email":request.form['email'],
            "phone":request.form['phone'],
            "password":request.form['password'],
            "role_id":request.form['role_id'],
            "created_by":request.form['created_by']
        }
        return authobj.signin(data)
    except Exception as e:
        return make_response(jsonify({"ERROR":"CONTACT_DEVELOPER_CONTROLLER"}), 200)
    
@app.route("/auth/unique_user/<key>/<value>", methods=["GET"])
def unique_user(key, value):
    if key=="email" or key=="phone":
        return make_response(jsonify({"ERROR":"USER_EXISTS", "keyname":key})) if authobj.unique_user(key, value) else make_response(jsonify({"SUCCESS":"NEW_USER", "keyname":key}))
    else:
        return make_response(jsonify({"ERROR":"INVALID_KEY"}))
    