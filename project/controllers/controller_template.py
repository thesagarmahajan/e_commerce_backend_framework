from imports import *
# Importing Model (Business Login)
# from project.models.admins_model import admins_model
# Initializing Obejct of imported model class
# adminobj = admins_model()
role_conf = app.config['custom_config']['roles_config']

@app.route('/path/')
@token_authenticator()
def function():
    return "function"
    # return adminobj.function()