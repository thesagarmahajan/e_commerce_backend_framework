from imports import *

from project.models.orders_model import orders_model

obj = orders_model()
role_conf = app.config['custom_config']['roles_config']

# @app.route('/order/create_cart', methods=['post'])
# @token_authenticator(role_conf['all'])
# def create_cart():
#     try:
#         postdata = json.loads(request.form['data'])
#         postdata['shipment_status'] = ""
#         postdata['payment_status'] = ""
#         postdata['expected_delivery'] = ""
#     except Exception as e:
#         return make_response({"ERROR":str(e), "FROM":"orders_controller"}) 
#     data = {
#         "created_by":tokendata['id'],
#         "data":json.dumps(postdata)
#     }
#     return obj.create_cart(data)

@app.route('/order/add_to_cart/<uid>', methods=['post'])
@token_authenticator(role_conf['all'])
def add_to_cart(uid):
    try:
        postdata = json.loads(request.form['data'])
    except Exception as e:
        return make_response({"ERROR":str(e), "FROM":"orders_controller"}) 
    
    if tokendata['rolename'] == 'admin':
        data = {
            "created_by":tokendata['id'],
            "customer_id":uid,
            "data":json.dumps(postdata)
        }
    else:
        data = {
            "created_by":tokendata['id'],
            "customer_id":tokendata['id'],
            "data":json.dumps(postdata)
        }
        
    return obj.add_to_cart(data)


@app.route('/order/place_order/<uid>/<orderid>')
@token_authenticator(role_conf['all'])
def place_order(uid, orderid):
    #  Change status=P (Pending)
    if tokendata['id']==uid or tokendata['rolename']=='admin':
        return obj.place_order(uid, orderid)
    else:
        return make_response({"ERROR":"INVALID_ROLE"})


@app.route('/order/process_payment/<uid>/<orderid>')
@token_authenticator(role_conf['all'])
def process_payment(uid, orderid):
    #  if payment method is POD then: status=A (Active), paymentStatus=Pending, shipmentStatus=orderConfirmed
    #  if payment method is Online and payment Success: Status=A (Active), paymentStatus=received, shipmentStatus=order_confirmed
    #  if payment method is Online and payment Failed: Status=P (Active), paymentStatus=failed, shipmentStatus=payment_processing   
    if tokendata['id']==uid or tokendata['rolename']=='admin':
        return obj.place_order(uid, orderid)
    else:
        return make_response({"ERROR":"INVALID_ROLE"})

@app.route('/order/update_shipment_status/<shipment_status>/<orderid>')
@token_authenticator(role_conf['admin_only'])
def update_shipment_status(shipment_status, orderid):
    # if shipment_status=preparing_to_ship then: update shipment_status
    # if shipment_status=shipped then: update shipment_status and expected_delivery=some date
    # if shipment_status=delivered then: update shipment_status and status=E (Completed)
    return obj.place_order(shipment_status, orderid)
    
    

# Listing data of all users
@app.route('/order/list_all')
@token_authenticator(role_conf['admin_only'])
def list_all_orders():
    return obj.list_all_orders()

@app.route('/order/list_all_active')
@token_authenticator(role_conf['admin_only'])
def list_all_active_orders():
    return obj.list_all_active_orders()

@app.route('/order/list_all_completed')
@token_authenticator(role_conf['admin_only'])
def list_all_completed_orders():
    return obj.list_all_completed_orders()

@app.route('/order/list_all_pending')
@token_authenticator(role_conf['admin_only'])
def list_all_pending_orders():
    return obj.list_all_pending_orders()

@app.route('/order/list_all_cancelled')
@token_authenticator(role_conf['admin_only'])
def list_all_cancelled_orders():
    return obj.list_all_cancelled_orders()

# Listing data of given or loggedin user
@app.route('/order/list_my_orders/<uid>')
@token_authenticator(role_conf['all'])
def list_my_orders(uid):
    if tokendata['rolename'] == 'admin':
        return obj.list_my_orders(uid)
    elif int(tokendata['id'])==int(uid):
        return obj.list_my_orders(uid)
    else:
        return make_response({"ERROR":"ID_MISMATCHED"})
    

@app.route('/order/list_my_e_orders/<uid>')
@token_authenticator(role_conf['all'])
def list_my_active_orders(uid):
    if tokendata['rolename'] == 'admin':
        return obj.list_my_active_orders(uid)
    elif int(tokendata['id'])==int(uid):
        return obj.list_my_active_orders(uid)
    else:
        return make_response({"ERROR":"ID_MISMATCHED"})

@app.route('/order/list_my_completed_orders/<uid>')
@token_authenticator(role_conf['all'])
def list_my_completed_orders(uid):
    if tokendata['rolename'] == 'admin':
        return obj.list_my_completed_orders(uid)
    elif int(tokendata['id'])==int(uid):
        return obj.list_my_completed_orders(uid)
    else:
        return make_response({"ERROR":"ID_MISMATCHED"})

@app.route('/order/list_my_pending_orders/<uid>')
@token_authenticator(role_conf['all'])
def list_my_pending_orders(uid):
    if tokendata['rolename'] == 'admin':
        return obj.list_my_pending_orders(uid)
    elif int(tokendata['id'])==int(uid):
        return obj.list_my_pending_orders(uid)
    else:
        return make_response({"ERROR":"ID_MISMATCHED"})

@app.route('/order/list_my_cancelled_orders/<uid>')
@token_authenticator(role_conf['all'])
def list_my_cancelled_orders(uid):
    if tokendata['rolename'] == 'admin':
        return obj.list_my_cancelled_orders(uid)
    elif int(tokendata['id'])==int(uid):
        return obj.list_my_cancelled_orders(uid)
    else:
        return make_response({"ERROR":"ID_MISMATCHED"})