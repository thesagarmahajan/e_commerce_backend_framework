from imports import *

class auth_model:
    
    def __init__(self):
        try:
            cconf = app.config['custom_config']['dbconf']
            self.con = psycopg2.connect(dbname=cconf['dbname'], user=cconf['dbuser'], host=cconf['dbhost'], password=cconf['dbpassword'], port=cconf['dbport'])
            self.con.set_session(autocommit=True)
            self.cur = self.con.cursor(cursor_factory=RealDictCursor)
        except psycopg2.DatabaseError as e:
            print(e)
        
    def password_decode(self, password):
        try:
            return b64decode(password)[::-1]
        except Exception as e:
            return e
        
    def generate_token(self, data,*args, **kwargs):
        token = jwt.encode({'data':data, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return token
    
    def password_based(self, role, email, password):
        if role=="admin":
            view_name = "admins_view"
            role_id = ""
            rolename = "admin"
        elif role=="user":
            view_name = "users_view"
            role_id = ", role_id"
            self.cur.execute("SELECT rolename FROM users_and_roles WHERE email='"+email+"' and status = 'A'")
            try:
                role_data = self.cur.fetchall()[0]
                rolename = role_data['rolename']
            except:
                return {"ERROR":"NO_ACTIVE_USERS"}
        else:
            return {"ERROR":"INVALID_ROLE"}
        
        self.cur.execute("SELECT id, full_name "+role_id+" from "+view_name+" where status='A' and password='"+password+"' and email='"+email+"'")
        usersdata = self.cur.fetchall()
        if(len(usersdata)==1):
            usersdata = usersdata[0]
            resp = usersdata
            resp['rolename'] = rolename
            resp["token"] = self.generate_token(json.dumps(usersdata))
            return resp
        else:
            return {"ERROR":"USERNAME_PASSWORD_MISMATCHED"}
    
    def send_otp(self):
        # Use MSG91 API to send OTP over SMS as well as Email
        print("SEND_OTP")
        
    def varify_otp(self, uid, otp):
        # Use MSG91 API to varify the OTP
        print("VARIFY_OTP")
    
    def signin(self, data):
        try:
            self.cur.execute("SELECT id from users_view WHERE phone='"+data['phone']+"'")
            if len(self.cur.fetchall()) > 0:
                return make_response(jsonify({"ERROR":"USER_EXISTS"}), 200)
            else:
                self.cur.execute("INSERT INTO users (status, data) VALUES(%s, %s)", ('P', json.dumps(data)))
                self.cur.execute("SELECT id from users_view WHERE phone='"+data['phone']+"'")
                result = self.cur.fetchall()
                latest_id = result[0]['id']
                return make_response(jsonify({"SUCCESS":"SUCCESS", "latest_user_id":latest_id}), 200)
        except Exception as e:
            return make_response({"ERROR":str(e)},500)
        
    
    def unique_user(self, key, value):
        try:
            self.cur.execute("SELECT id from users_view WHERE "+key+" ='"+value+"'")
            return True if len(self.cur.fetchall()) > 0 else False
        except:
            return False
            
    def __del__(self):
        self.con.close()