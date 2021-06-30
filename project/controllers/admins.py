from imports import *

# Importing Model (Business Login)
from project.models.admins_model import admins_model
# Initializing Obejct of imported model class
adminobj = admins_model()
role_conf = app.config['custom_config']['roles_config']

@app.route('/admins/get_all_resellers/')
@token_authenticator(role_conf['admin_only'])
def get_all_resellers():
    return adminobj.get_all_resellers()

@app.route('/admins/add_product/', methods=['POST'])
@token_authenticator(role_conf['admin_only'])
def add_product():
    return "This is add product"

@app.route('/admins/add_category/', methods=['POST'])
@token_authenticator(role_conf['admin_only'])
def add_category():
    return "This is add category"

@app.route('/admins/add_role/', methods=['POST'])
@token_authenticator(role_conf['admin_only'])
def add_role():
    return "This is add role"

@app.route('/admins/get_reseller_data/<reseller_id>', methods=['GET'])
@token_authenticator(role_conf['admin_only'])
def get_reseller_data(reseller_id):
    return "This is get reseller data"

@app.route('/admins/deactivate_reseller/')
@token_authenticator(role_conf['admin_only'])
def deactivate_reseller():
    return "This is update deactivate reseller"
