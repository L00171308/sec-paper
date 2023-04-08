
import mysql.connector

# change connection info
conn = mysql.connector.connect(
    host="test",
    database="test",
    user="admin",
    password="admin")

cur = conn.cursor()

def check_db():
    """
    If the database is empty, create the tables and seed the database.
    """
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
    data = cur.fetchall()
    if data == []:
        try:
            cur.execute("CREATE TABLE users (email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), role VARCHAR(255));")
            cur.execute("CREATE TABLE grants (name VARCHAR(255) PRIMARY KEY, ammount INT, site VARCHAR(255));")
            cur.execute("CREATE TABLE applications (name VARCHAR(255) PRIMARY KEY, grant_name VARCHAR(255), ammount INT);")
            
        except:
            print("I can't create the table")
    cur.execute("SELECT * FROM users ")
    data = cur.fetchall()
    if data == []:
        cur.execute("SELECT * FROM grants ")
        data = cur.fetchall()
        if data == []:
            seed_db()


    



def seed_db():
    """
    It takes the data from the user_data and grant_data lists and inserts it into the users and grants
    tables in the database
    """
    query_user= """ INSERT INTO users (email, password, role) VALUES (%s,%s,%s)"""
    query_grant= """ INSERT INTO grants (name, ammount, site) VALUES (%s,%s,%s)"""
    user_data= [
        {
        "email":"admin@test.com",
        "password":"admin",
        "role":"admin"
        },
        {
        "email":"aidan@test.com",
        "password":"admin",
        "role":"admin"
        },
        {
        "email":"anuradha@test.com",
        "password":"admin",
        "role":"admin"
        },
        {
        "email":"rotimi@test.com",
        "password":"admin",
        "role":"admin"
        },
        {
        "email":"samantha@test.com",
        "password":"admin",
        "role":"admin"
        },
        {
        "email":"dean@test.com",
        "password":"admin",
        "role":"admin"
        }
        ]
    grant_data= [
        {
        "name":"Help to Buy Scheme",
        "ammount":30000,
        "site":"https://www.citizensinformation.ie/en/housing/owning_a_home/help_with_buying_a_home/help_to_buy_incentive.html"
        },
        {
        "name":"Future Growth Loan Scheme",
        "ammount":80000000,
        "site":"https://enterprise.gov.ie/en/What-We-Do/Supports-for-SMEs/Access-to-Finance/Future-Growth-Loan-Scheme/"
        }
        ]
    for i in user_data:
        record = (i['email'], i['password'], i['role'])
        cur.execute(query_user, record)
        conn.commit()
    for i in grant_data:
        record = (i['name'],i['ammount'],i['site'])
        cur.execute(query_grant, record)
        conn.commit()

check_db()

def register_user(username=None, password=None):
    """
    It takes a username and password as arguments, and inserts them into the database
    
    :param username: The username of the user you want to register
    :param password: the password you want to use
    """
    insert_stmt = (
        "INSERT INTO users (email, password, role) "
        "VALUES (%s, %s, %s)"
    )
    data = (username, password, "user")
    cur.execute(insert_stmt, data)
    conn.commit()


def patch_user(username=None, password=None, newuser=None, newpass=None):
    """
    It takes in a username and password, and if the username is not in the database, it registers the
    user. If the username is in the database, it updates the password
    
    :param username: The username of the user you want to update
    :param password: The password of the user you want to change
    :param newuser: The new username
    :param newpass: The new password you want to set for the user
    """
    sql = "SELECT * FROM users WHERE email = %s"
    adr = (username, )
    cur.execute(sql, adr)
    if len(cur.fetchall()) == 0:
        register_user(username, password)
    else:
        sql = "UPDATE users SET email = %s WHERE email = %s"
        val = (newuser, newpass)
        cur.execute(sql, val)
        conn.commit()


def remove_user(username=None):
    """
    It deletes a user from the database
    
    :param username: The username of the user you want to remove
    """
    sql = "DELETE FROM users WHERE name = %s"
    adr = (username, )
    cur.execute(sql, adr)
    conn.commit()


# todo: add,remove,update grants method

def add_app(name=None, grant_name=None, ammount=None):
    """
    It takes three arguments, and inserts them into the database
    
    :param name: The name of the grant
    :param ammount: The ammount of money the grant is worth
    :param site: The site where the grant is located
    """
    insert_stmt = (
        "INSERT INTO grants (name, grant_name, ammount) "
        "VALUES (%s, %s, %s)"
    )
    data = (name, grant_name, ammount)
    cur.execute(insert_stmt, data)
    conn.commit()


def add_grant(name=None, ammount=None, site=None):
    """
    It takes three arguments, and inserts them into the database
    
    :param name: The name of the grant
    :param ammount: The ammount of money the grant is worth
    :param site: The site where the grant is located
    """
    insert_stmt = (
        "INSERT INTO grants (name, ammount, site) "
        "VALUES (%s, %s, %s)"
    )
    data = (name, ammount, site)
    cur.execute(insert_stmt, data)
    conn.commit()


def patch_grant(name=None, ammount=None, newname=None, newammount=None, newsite=None):
    """
    It takes in a name, ammount, newname, newammount, and newsite. It then checks if the name is in the
    database, if it is, it updates the name and ammount, if it isn't, it registers the newname,
    newammount, and newsite
    
    :param name: The name of the grant
    :param ammount: The ammount of money the grant is worth
    :param newname: The new name of the grant
    :param newammount: The new ammount of money the grant will have
    :param newsite: The new site that the grant is on
    """
    sql = "SELECT * FROM grants WHERE name = %s"
    adr = (name, )
    cur.execute(sql, adr)
    if len(cur.fetchall()) == 0:
        register_user(newname, newammount, newsite)
    else:
        sql = "UPDATE grants SET name = %s WHERE name = %s"
        val = (name, ammount)
        cur.execute(sql, val)
        conn.commit()


def remove_grant(name=None):
    """
    This function deletes a grant from the grants table in the database
    
    :param name: The name of the grant you want to remove
    """
    sql = "DELETE FROM grants WHERE name = %s"
    adr = (name, )
    cur.execute(sql, adr)
    conn.commit()


def getall_grants():
    """
    It returns all the rows from the grants table
    :return: A list of tuples.
    """
    sql = "SELECT * FROM grants"
    cur.execute(sql)
    return cur.fetchall()


def search(username = None, password = None):
    """
    It takes a username as an argument, and returns True if the username is in the database, and False
    if it isn't
    
    :param username: The username of the user you want to search for
    :return: True or False
    """
    
    sql = "SELECT * FROM users"
    cur.execute(sql,)
    for i in cur.fetchall():
        if str(username == i[0]):
            if str(password == i[1]):
                return True
    return False

    
    

    
def search_grant_ammount(name = None, ammount = None):
    """
    It takes a username as an argument, and returns True if the username is in the database, and False
    if it isn't
    
    :param username: The username of the user you want to search for
    :return: True or False
    """
    sql = "SELECT * FROM grants WHERE name = %s AND ammount = %s "
    adr = (name, ammount)
    cur.execute(sql, adr)
    if len(cur.fetchall()) == 1:
        return True
    else:
        return False

def getrole(username = None):
    """
    It takes a username as an argument, and returns the role of the user
    
    :param username: The username of the user you want to get the role of
    :return: A tuple of tuples.
    """
    sql = "SELECT role FROM users WHERE email = %s"
    adr = (username, )
    cur.execute(sql, adr)
    resp = cur.fetchall()
    if len(resp)>1:
        return "user"
    else:
        return str(resp[0])
