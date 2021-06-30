from imports import *

class admins_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)
            
    def get_all_resellers(self):
        try:
            self.cur.execute("SELECT *, to_char(created_on, 'YYYY-MM-DD HH24:MI:SS') as created_on FROM resellers_view")
            result = self.cur.fetchall()
            if len(result) > 0:
                return make_response({"data":result},200)
            else:
                return make_response({"NOT_FOUND":"NO_RECORDS_FOUND"},204)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    def __del__(self):
        self.con.close()
        