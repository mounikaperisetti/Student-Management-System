from config import Config
import mysql.connector as sql
import random
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, redirect, url_for, request, session
import bcrypt

app = Flask(__name__)
app.secret_key = "Mounik@03" # this help the session to validate  without this key cant cannot use sesssion useing key we can access values in session
# session is used when one page data is used in another page.. like from register 'email' to in verify 'email'
# we can store values in session.. soo lets take otp in session and remove otp from global
DBConfig = Config()
from_email = DBConfig.from_email
email_app_password = DBConfig.email_app_password

def getConnectionWithDB():
    db_host = DBConfig.db_host   # here .db_host is memeber variable wheree db_host = is a local variable
    db_port = DBConfig.db_port
    db_user = DBConfig.db_user
    db_password = DBConfig.db_password
    db_name = DBConfig.db_name 
    try:
        connection = sql.connect(
            host = db_host,
            port = db_port,
            user = db_user,
            password = db_password,
            database = db_name
        )
        return connection
    except:
        return 'Connection Failed'

def insertUserRecord(user_data):
    name = user_data['name']
    email = user_data['email']
    password_hash = user_data['password_hash']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        try:
            cursor = connection.cursor()  # here cursor is used to execute sql queries(ex:insert,etc.)
            cursor.execute("INSERT INTO users (name,email,password_hash) values(%s,%s,%s)",(name,email,password_hash))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except:
            print("same Email can't be entered again")
            return False
      
def readUserRecords():
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * from users")
        data = cursor.fetchall()  # here data is iterator object so here to access that iterator object u=you have to user for loop or list comprehension
        records = []
        for record in data:
            temp = {}
            temp['id'] = record[0]
            temp['name'] = record[1]
            temp['email'] = record[2]
            temp['password_hash'] = record[3]
            temp['is_verified'] = record[4]
            temp['created_at'] = record[5]
            records.append(temp)
        cursor.close()
        connection.close()
        return records

def readUserRecordByEmail(user_data):
    email = user_data['email']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * from users where email = %s",(email,))
        data = cursor.fetchone()
        try:
            record = {
                'id' : data[0],
                'name' : data[1],
                'email' : data[2],
                'password_hash' : data[3],
                'is_verified' : data[4],
                'created_at' : data[5]
            }
            cursor.close()
            connection.close()
            return record
        except:
            cursor.close()
            connection.close()
            return 'No record'

def readUserRecordById(user_data):
    id = user_data['id']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * from users where id = %s",(id,))
        data = cursor.fetchone()
        try:
            record = {
                'id' : data[0],
                'name' : data[1],
                'email' : data[2],                
                'password_hash' : data[3],
                'is_verified' : data[4],
                'created_at' : data[5]
            }
            cursor.close()
            connection.close()
            return record
        except:
            cursor.close()
            connection.close()
            return 'No record found for that id'

def updateNameByIdorEmail(user_data):
    query_filter = ''
    try:
        id = user_data['id']
        query_filter = 'id'
    except:
        email = user_data['email']
        query_filter = 'email'
    new_name = user_data['new_name']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        if query_filter == 'id':
            query = "UPDATE  users SET name = %s WHERE id = %s"
            values = (new_name,id)
        elif query_filter == 'email':
            query = "UPDATE  users SET name = %s WHERE email = %s"
            values = (new_name,email)       
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True

def updatePasswordByIdorEmail(user_data):
    query_filter = ''
    try:
        id = user_data['id']
        query_filter = 'id'
    except:
        email = user_data['email']
        query_filter = 'email'
    new_password = user_data['new_password']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        if query_filter == 'id':
            query = "UPDATE  users SET password_hash = %s WHERE id = %s"
            values = (new_password,id)
        elif query_filter == 'email':
            query = "UPDATE  users SET password_hash = %s WHERE email = %s"
            values = (new_password,email)       
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True

def updateIsVerifiedByIdorEmail(user_data):
    query_filter = ''
    try:
        id = user_data['id']
        query_filter = 'id'
    except:
        email = user_data['email']
        query_filter = 'email'
    is_verified = user_data['is_verified']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        if query_filter == 'id':
            query = "UPDATE  users SET is_verified = %s WHERE id = %s"
            values = (is_verified,id)
        elif query_filter == 'email':
            query = "UPDATE  users SET is_verified = %s WHERE email = %s"
            values = (is_verified,email)       
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        return True

def generateOTP():
    otp = random.randint(1000,9999)
    return otp

def sendOTPviaEmail(to_email,otp):
    # 1, to whom, we have to send OTP    ==> to address
    # 2, Through whhich acc we have to send OTP    ==> from address
    # 3, from - gmail LOGIN  - APP PASSWORD(here is is an encrypted password we have to create)
    # 4, Mail Compose
    # 4, Mail Send
    message = EmailMessage()
    message['Subject'] = 'OTP Notification'
    message['From'] = from_email
    message['To'] = to_email
    message.set_content(
        f"Your OTP is {otp}"
    )
    with smtplib.SMTP("smtp.gmail.com",587) as server:   # here with operater does is: whaterver obj is creaetd within the block the object destroys automatically  when its done
        server.starttls()
        server.login(from_email,email_app_password)
        server.send_message(message)
    return True

def validateDataForRegister(user_data):
    errors = []
    name = user_data['name']
    email = user_data['email']
    password = user_data['password']
    confirm_password = user_data['confirm_password']
    if name is None or len(name)<2 or '':
        errors.append("Invalid Name")
    if email is None or len(email)<5 or '':
        errors.append("Invalid Email")
    if password is None or len(password)<5 or '':
        errors.append("Invalid Passowrd")
    if password != confirm_password:
        errors.append( "Passwords do not match")
    return errors

def verifyDuplicateEmail(user_data):
    record = readUserRecordByEmail(user_data)
    if record == 'No record':
        return False   # no duplicate
    else:
        return True

# encode - Str to bytes
# decode - Bytes to Str
# gensalt - used to generate a key
# for gensalt we have pass how many this key to iterate
def generateHash(text):
    btext = text.encode('utf-8')     
    print(text[0],btext[0])    # here  text is string;  btext is bytes
    cypher_text =  bcrypt.hashpw(btext, bcrypt.gensalt(4))
    return cypher_text.decode('utf-8')

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    #request is GET {Browser}
    if (request.method=='GET'):
        # Display html file
        return render_template('register.html')
    # request is HTML FORM POST
    elif (request.method=='POST'):
        # Step 1: Input User data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_data={
            "name":name,
            "email":email,
            "password":password,
            "confirm_password":confirm_password    
        }
        # Step-2: Validate the suer data
        errors = validateDataForRegister(user_data)
        if len(errors) > 0:
            # if errors exist, display errors
            return render_template('register.html',errors=errors)
        else:
            # if no errors, start business logic:
            # 1, check weather acc exist on this email or not
            is_duplicate = verifyDuplicateEmail(user_data)
            if is_duplicate == False:
                # 2, if there is no acc 
                # 3, convert password to hash value
                ######  here lets create session ###########
                OTP = generateOTP()          # 
                password_hash = generateHash(user_data['password'])
                # 4, inserting this data into table
                name = user_data['name']
                email = user_data['email']
                status = insertUserRecord({
                    'name': name,
                    'email' : email,
                    'password_hash' : password_hash
                })
                # 4, status of insertion
                if status == True:  
                    session['username'] = email     ## here theese session can be access anywhere until its logot.. lets see this session in verify
                    session['otp'] = OTP
                    sendOTPviaEmail(email,OTP)
                    # return render_template('register.html', res = 'Registration Successfully Completed')
                    return redirect('/verify')
                else:
                    return render_template('register.html', err = "Registration Failed")
            else:
                return render_template('register.html', err = "Account Already Exist")

@app.route('/verify',methods=['GET','POST'])
def verify():
    if request.method == 'GET':
        return render_template('verify.html')
    elif (request.method == 'POST'):
        otp = request.form['otp']
        otp = int(otp)   # here this otp is stored in server side ram 
        if otp == session['otp']:  ## here we take the session['otp'] which is from register page  se here the entered otp and the otp generated are equal lets change record i mean is_verified and update it in table
            # here session['otp'] is stored in client side browser side memory 
            
            updateIsVerifiedByIdorEmail({'email' : session['username'],'is_verified' : True})  # here the datatype of argument is string.. and datatype of session is dictionary
            return redirect('/login')
        else:
            return render_template('verify.html', err = "Invalid OTP")

#-------------- Registration flow ---------------#
# Register.html <-> Registration form ->POST <-> Python -> CO=ollection Data ->Validating -> Password to Password HAsh -<> MySQL Table
# name,email,password,COnform password and submit
# verifyduplicateEmai() - if acc not existed
# generate otp
# send email with otp
# redirect to verify.html
# enter otp received from email
#the otp  entered with session otp
# if they are matched, it redirects to login .html
# if they are not matched, it redirects with a rerros message

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        # we have to check acc existed or not
        # if data exist, then we have to check is_verified is True or False
        # if acc exist and verified, then compare passwords
        # if password is equal then create session.. inside session we have to store email
        user_data = readUserRecordByEmail({'email': email})
        if user_data == 'No record':
            return render_template('login.html', err = "Email Not exist")
        elif user_data['is_verified'] == False:
            return render_template('login.html', err = "Please Verify you account")
        elif bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')) == False:
            return render_template('login.html', err = "Password do not match")
        else:
            session['username'] = user_data['name']
            session['email'] = email
            return redirect('/dashboard')     

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


          
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    email = session['email']
    username = session['username']
    user_data = readUserRecordByEmail({'email':email})
    if user_data == 'No record':
        session.clear()
        return redirect('/login')
    user_id = user_data['id']
    user_name = user_data['name']
    connection = getConnectionWithDB()
    if connection == 'Connection Failed':
        return False
    else:
        cursor = connection.cursor()
        # total notes 
        cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = %s",(user_id,))
        total_notes = cursor.fetchone()[0]
        # total files
        cursor.execute("SELECT COUNT(*) FROM file_data WHERE user_id = %s",(user_id,))
        total_files = cursor.fetchone()[0]
        # recent_files
        cursor.execute("SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",(user_id,))
        notes_data = cursor.fetchall()
        cursor.close()
        connection.close()
        #convert tuple data into dictinaries
        notes = []
        for note in notes_data:
            notes.append({

                'id': note[0],
                'title': note[2],
                'content': note[3],
                'created_at': note[4],
                'updated_at': note[5]
            })
        return render_template(
            'dashboard.html', 
            username = username,
            total_notes = total_notes,
            total_files = total_files,
            notes = notes
            )

    


if(__name__ == '__main__'):
    app.run(
        host = '0.0.0.0',
        port = 5000,
        debug = True
    )
