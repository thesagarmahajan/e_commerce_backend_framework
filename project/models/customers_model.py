from imports import *
class customers_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)
            
    
    def add_customer(self):
        return make_response({"SUCCESS":"This is add Customer"})