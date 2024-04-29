from flask import Flask,render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_mail import *
import json
import mysql.connector
import os

app=Flask(__name__)
app.secret_key= os.urandom(20)

conn=mysql.connector.connect(host="localhost", user="root", password="", database="mydatab")
cursor=conn.cursor()

# to extract data from config.json file

with open('config.json','r') as f:
    par=json.load(f)['parametres']


# to check the database connection

def check_mysql_connection():
    try:
        chk_cursor = mysql.connection.cursor()
        chk_cursor.execute("SELECT 1")
        result = chk_cursor.fetchone()
        if result:
            return "Connected to MySQL database."
        else:
            return "Error connecting to MySQL database."
    except Exception as e:
        return f"Error connecting to MySQL database: {e}"



# For showing the login.html page as the firstpage and giving a /home name to index.html

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/reg')
def regis():
    return render_template('register.html')



#fetching data from login and validating login data

@app.route('/login_accnt', methods=["POST"])
def login_accnt():
    ln_username=request.form["email"]
    ln_password=request.form["password"]
        
    cursor.execute("SELECT * FROM login_table WHERE email= %s AND password= %s", (ln_username, ln_password))
    exist_user=cursor.fetchall()
    if len(exist_user)>0:
        session['user_id']=exist_user[0][0]
        return redirect('/home')
    else:
        return redirect('/') 
    
    
 
 #fetching data from registration portal 
   
@app.route('/register_accnt', methods=["POST"])
def register_accnt():
    
    reg_user=request.form["reg_username"]
    reg_mail=request.form["reg_email"]
    reg_pass=request.form["reg_password"]
    cursor.execute("INSERT INTO login_table(NAME, EMAIL, PASSWORD) VALUES(%s, %s, %s)", (reg_user, reg_mail, reg_pass))
    conn.commit()
    
    cursor.execute("SELECT * FROM login_table WHERE email= %s", (reg_mail,))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect("/reg")
    

    
# For online table reservation part
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatab'

mysql= MySQL(app)

@app.route('/postdata', methods=['POST'])
def submit():
    if request.method=='POST':
        name=request.form["name"]
        ph=request.form["phone"]
        pers=request.form["person"]
        dt=request.form["reservation-date"]
        time=request.form["time"]
        msg=request.form["message"]
        
        print(name,ph,pers,dt,time,msg)
    
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO user_table(NAME, PHONE, PERSON, DATE, TIME, MESSAGE) VALUES (%s, %s, %s, %s, %s, %s)", (name, ph, pers, dt, time, msg))
        mysql.connection.commit()
        cur.close()
        
        return "Your Table has been booked"
    else:
        return "Something went wrong"
    
  
    
# For email subscription part

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=par['gmail-user']
app.config['MAIL_PASSWORD']=par['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

@app.route('/submail', methods=['POST','GET'])
def index():
    if request.method=='POST':
        email_id=request.form["email_address"]
        msg=Message('Subscription mail', sender=par['gmail-user'], recipients=[email_id])
        msg.body="Welcome to the world of Spice_Symphony. Hope you will enjoy our dishes that will be served with extravagant Indian spices making the dishes extremely flavourful. "
        mail.send(msg)
        return "Message Sent"
    else:
       return "Sorry! message cannot be sent" 
 
 
# for logging out of an account
 
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)