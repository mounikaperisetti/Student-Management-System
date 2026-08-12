from config import Config
import mysql.connector as sql

DBConfig = Config()

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
        cursor = connection.cursor()  # here cursor is used to execute sql queries(ex:insert,etc.)
        cursor.execute("insert into users (name,email,password_hash) values(%s,%s,%s)",(name,email,password_hash))
        connection.commit()
        cursor.close()
        connection.close()
        return True
data = {
    'name' : 'Tony',
    'email' : 'Tony@gmail.com',
    'password_hash' : '1a2b3c'
}
print(insertUserRecord(data))