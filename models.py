import pymysql


def insertUser(email,password,fname,lname,phone):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select userid from user where email=%s",(email))
    exist = cur.fetchall()
    success = 0
    if len(exist) == 0:
        cur.execute("INSERT INTO user (email,password,first_name,last_name,phone) VALUES (%s,%s,%s,%s,%s)",
        (email,password,fname,lname,phone))
        con.commit()
        con.close()
        success = 1
    else:
         success = 0
    return success

def getPassword(email):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("SELECT password,first_name FROM user where email= %s", (email))
    result = cur.fetchall()
    con.close()
    return result
	
def insertPatient(fname,lname,email,gender,age,phone,race):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select patientid from patients where email=%s",(email))
    exist = cur.fetchall()
    success = 0
    if len(exist) == 0:
        cur.execute("INSERT INTO patients (first_name,last_name,email,gender,age,phone,race) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (fname,lname,email,gender,age,phone,race))
        con.commit()
        con.close()
        success = 1
    else:
         success = 0
    return success
	
def getPatientInfo(fname):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select * from patients where first_name=%s",(fname))
    patients = cur.fetchall()
    return patients
	
def UpdatePatient(fname,lname,gender,age,phone,race):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select patientid from patients where email=%s",(email))
    exist = cur.fetchall()
    success = 0
    if len(exist) == 0:
        cur.execute("INSERT INTO patients (first_name,last_name,email,gender,age,phone,race) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (fname,lname,email,gender,age,phone,race))
        con.commit()
        con.close()
        success = 1
    else:
         success = 0
    return success