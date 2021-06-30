from imports import *
# Importing Model (Business Login)
from project.models.categories_model import categories_model
# Initializing Obejct of imported model class
obj = categories_model()
role_conf = app.config['custom_config']['roles_config']

@app.route('/category/list_all/')
@token_authenticator()
def list_all_categories():
    return obj.list_all_categories()

@app.route('/category/add_new/', methods=['POST'])
@token_authenticator(role_conf['admin_only'])
def add_new_category():
    data={
        "created_by":tokendata['id'],
        "data":request.form['data']
    }
    return obj.add_new_category(data)

@app.route('/category/delete/<cat_id>')
@token_authenticator(role_conf['admin_only'])
def delete_category(cat_id):
    return obj.delete_category(cat_id)

@app.route('/category/get_details/<cat_id>')
@token_authenticator(role_conf['admin_only'])
def get_category_details(cat_id):
    return obj.get_category_details(cat_id)

