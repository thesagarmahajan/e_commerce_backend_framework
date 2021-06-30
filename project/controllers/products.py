from imports import *
import os
from werkzeug.utils import secure_filename
import time
# Importing Model (Business Login)
from project.models.products_model import products_model
# Initializing Obejct of imported model class
obj = products_model()
role_conf = app.config['custom_config']['roles_config']

@app.route('/product/list_all/')
@token_authenticator(role_conf['admin_only'])
def list_all_products():
    return obj.list_all_products()

@app.route('/product/count_active/')
def count_active_products():
    return obj.count_active_products()

@app.route('/product/list_all_active/')
# @token_authenticator()
def list_all_active_products():
    return obj.list_all_active_products()

@app.route('/product/list_all_pending/')
@token_authenticator(role_conf['admin_only'])
def list_all_pending_products():
    return obj.list_all_pending_products()

@app.route('/product/list_all_deleted/')
@token_authenticator(role_conf['admin_only'])
def list_all_deleted_products():
    return obj.list_all_deleted_products()

@app.route('/product/get_details/<pid>')
# @token_authenticator()
def get_product_details(pid):
    return obj.get_product_details(pid)

@app.route('/product/upload_image/', methods=['POST'])
# @token_authenticator(role_conf['admin_only'])
def upload_product_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1]
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    if extension in allowed_extensions:
        extension = os.path.splitext(filename)[1]
        currenttime = time.time()
        finalfile = str(currenttime).split(".")[0]+str(currenttime).split(".")[1]+extension
        file.save(os.path.join(app.root_path+"/uploads", finalfile))
        return make_response({"SUCCESS":"FILE_UPLOADED", "FILE_PATH":finalfile},200)
    else:
        return make_response({"ERROR":"FILE_EXTENSION_NOT_SUPPORTED"}, 200)
 
@app.route('/product/get_image/<imagepath>')
# @token_authenticator(role_conf['admin_only'])
def get_image(imagepath):
    return send_file(app.root_path+"/uploads/"+imagepath)
    

@app.route('/product/add_new/', methods=['POST'])
@token_authenticator(role_conf['admin_only'])
def add_new_product():
    data={
        "created_by":tokendata['id'],
        "data":request.form['data']
    }
    return obj.add_new_product(data)

@app.route('/product/make_active/<pid>')
@token_authenticator(role_conf['admin_only'])
def make_product_active(pid):
    return obj.make_product_active(pid)

@app.route('/product/delete/<pid>')
@token_authenticator(role_conf['admin_only'])
def delete_product(pid):
    return obj.delete_product(pid)







