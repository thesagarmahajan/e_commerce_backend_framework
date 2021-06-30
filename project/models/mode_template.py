# from imports import *
# class model_name:
    
#     def __init__(self):
#         try:
#             cconf = app.config['custom_config']['dbconf']
#             self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
#             self.con.set_session(autocommit=True)
#             self.cur = self.con.cursor(cursor_factory=RealDictCursor)
#         except psycopg2.DatabaseError as e:
#             print(e)