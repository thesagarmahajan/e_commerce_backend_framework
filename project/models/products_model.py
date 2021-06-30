from imports import *
class products_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)
    
    
    def list_all_products(self):
        try:
            self.cur.execute("SELECT * FROM products_view")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def count_active_products(self):
        try:
            self.cur.execute("SELECT COUNT(ID) FROM products_view WHERE status='A'")
            result = self.cur.fetchall()
            if len(result) > 0:
                print(result)
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_active_products(self):
        try:
            self.cur.execute("SELECT * FROM products_view WHERE status='A'")
            result = self.cur.fetchall()
            if len(result) > 0:
                print(result)
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    def list_all_pending_products(self):
        try:
            self.cur.execute("SELECT * FROM products_view WHERE status='P'")
            result = self.cur.fetchall()
            if len(result) > 0:
                print(result)
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def list_all_deleted_products(self):
        try:
            self.cur.execute("SELECT * FROM products_view WHERE status='D'")
            result = self.cur.fetchall()
            if len(result) > 0:
                print(result)
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def get_product_details(self, pid):
        try:
            self.cur.execute("SELECT * FROM products_view WHERE status='A' and id="+pid)
            result = self.cur.fetchall()
            if len(result) > 0:
                print(result)
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    def add_new_product(self, data):
        try:
            self.cur.execute("INSERT INTO products (created_by, status, data) VALUES(%s, %s, %s)", (data['created_by'], 'P', data['data']))
            return make_response({"SUCCESS":"product_ADDED"},200)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    def make_product_active(self, pid):
        try:
            self.cur.execute("UPDATE products SET status='A' WHERE id="+pid)
            return make_response({"SUCCESS":"PRODUCT_ACTIVATED"}, 200)
        except Exception as e:
            return make_response({"ERROR":str(e)}, 200)
    
    def delete_product(self, pid):
        try:
            self.cur.execute("UPDATE products SET status='D' WHERE id="+pid)
            return make_response({"SUCCESS":"PRODUCT_DELETED"}, 200)
        except Exception as e:
            return make_response({"ERROR":str(e)}, 200)