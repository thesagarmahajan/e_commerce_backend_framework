from imports import *
class orders_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)

        
    def add_to_cart(self, data):
        try:
            self.cur.execute("SELECT ID FROM all_orders_view WHERE status='K' AND created_by="+str(data['created_by']))
            result = self.cur.fetchall()
            if len(result) == 1:
                print(data)
                update_details = json.loads(data['data'])['details'][0]
                final_total = json.loads(data['data'])['final_total']
                grand_total = json.loads(data['data'])['grand_total']
                print(update_details)
                self.cur.execute("UPDATE orders set data=jsonb_set(data::jsonb, CONCAT('{details,',json_array_length(data->'details'),'}')::text[], '"+json.dumps(update_details)+"')  where created_by="+str(data['created_by']))
                self.cur.execute("UPDATE orders set data=jsonb_set(data::jsonb, '{final_total}', (COALESCE(data->>'final_total','0')::int + "+str(final_total)+")::text::jsonb) where created_by="+str(data['created_by']));
                self.cur.execute("UPDATE orders set data=jsonb_set(data::jsonb, '{grand_total}', (COALESCE(data->>'grand_total','0')::int + "+str(grand_total)+")::text::jsonb) where created_by="+str(data['created_by']));
                return make_response({"SUCCESS":"CART_UPDATED"},200)
            elif len(result) > 1:
                return make_response({"ERROR":"TWO_CART_EXISTS", "data":result},200)
            else:
                # Create New cart and add this item
                # data = json.loads(data)
                details = json.loads(data['data'])
                details['shipment_status'] = ""
                details['payment_status'] = ""
                details['expected_delivery'] = ""
                details['discount'] = 0
                details['payment_type'] = ""
                details['customer_id'] = data['customer_id']
                self.cur.execute("INSERT INTO orders (created_by, status, data) VALUES(%s, %s, %s)", (data['created_by'], 'K', json.dumps(details)))
                return make_response({"SUCCESS":"CART_INIT"},200)
        except Exception as e:
            return make_response({"ERROR":str(e), "from":"add_to_cart"},500)
    
    def place_order(self, uid, orderid):
        try:
            #  Change status=P (Pending)
            return make_response({"SUCCESS":"This is place order function"},200)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def process_payment(self, uid, orderid):
        try:
            #  if payment method is POD then: status=A (Active), paymentStatus=Pending, shipmentStatus=orderConfirmed
            #  if payment method is Online and payment Success: Status=A (Active), paymentStatus=received, shipmentStatus=order_confirmed
            #  if payment method is Online and payment Failed: Status=P (Active), paymentStatus=failed, shipmentStatus=payment_processing
            return make_response({"SUCCESS":"This is process_payment function"},200)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def update_shipment_status(self, shipment_status, orderid):
        # if shipment_status=preparing_to_ship then: update shipment_status
        # if shipment_status=shipped then: update shipment_status and expected_delivery=some date
        # if shipment_status=delivered then: update shipment_status and status=E (Completed)
        return make_response({"SUCCESS":"This is update_shipment_status function"},200)
        
    # Listing data of all users
    def list_all_orders(self):
        try:
            self.cur.execute("SELECT * FROM all_orders_view")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_active_orders(self):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='A'")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_completed_orders(self):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='E'")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_pending_orders(self):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='P'")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_cancelled_orders(self):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='C'")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    # Listing data of given or loggedin user
    def list_my_orders(self, uid):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE created_by="+uid)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    def list_my_active_orders(self, uid):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='A' and created_by="+uid)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_my_completed_orders(self, uid):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='E' and created_by="+uid)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_my_pending_orders(self, uid):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='P' and created_by="+uid)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_my_cancelled_orders(self, uid):
        try:
            self.cur.execute("SELECT * FROM all_orders_view WHERE status='C' and created_by="+uid)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)