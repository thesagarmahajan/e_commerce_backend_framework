from imports import *

from project.models.customers_model import customers_model

obj = customers_model()
role_conf = app.config['custom_config']['roles_config']

@app.route('/customer/add')
@token_authenticator()
def add_customer():
    return obj.add_customer()