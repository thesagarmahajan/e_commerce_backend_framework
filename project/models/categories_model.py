from imports import *
class categories_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)
                
    def list_all_categories(self):
        try:
            self.cur.execute("SELECT * FROM categories_view WHERE status='A'")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def add_new_category(self, data):
        try:
            self.cur.execute("INSERT INTO categories (created_by, status, data) VALUES(%s, %s, %s)", (data['created_by'], 'A', data['data']))
            return make_response({"SUCCESS":"CATEGORY_ADDED"},201)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
    
    def delete_category(self, cat_id):
        try:
            self.cur.execute("UPDATE categories SET status='A' WHERE id="+cat_id)
            return make_response({"SUCCESS":"CATEGORY_DELETED"}, 200)
        except Exception as e:
            return make_response({"ERROR":str(e)}, 500)
        
    def get_category_details(self, cat_id):
        try:
            self.cur.execute("SELECT * FROM categories_view WHERE id="+cat_id)
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)