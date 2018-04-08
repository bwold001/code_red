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
    cur.execute("SELECT password,first_name,userid FROM user where email= %s", (email))
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
	
def getPatientInfo(email):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select * from patients where email=%s",(email))
    patients = cur.fetchall()
    con.close()
    return patients

def getUserInfo(user_id):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select * from user where userid=%s",(user_id))
    user_info = cur.fetchall()
    con.close()
    return user_info
	
def getPatientInfoByID(p_id):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select * from patients where patientid=%s",(p_id))
    patients = cur.fetchall()
    return patients
	
def updatePatient(patient_id,fname,lname,gender,phone,race):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("UPDATE patients SET first_name = %s,last_name =%s, gender = %s, phone=%s, race=%s WHERE patientid=%s",
				(fname,lname,gender,phone,race,patient_id))
    con.commit()
    con.close()
    success = 1
    return success

def updateUserProfile(usr_id,fname,lname,phone,password):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    if not password:
        cur.execute("UPDATE user SET first_name = %s,last_name =%s, phone = %s WHERE userid=%s",
                   (fname,lname,phone,usr_id))
    else:
        cur.execute("UPDATE user SET first_name = %s,last_name =%s, phone = %s, password=%s WHERE userid=%s",
                   (fname,lname,phone,password,usr_id))
    con.commit()
    con.close()
    success = 1
    return success
	
def getRecents():
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("SELECT * FROM patients ORDER BY patientid DESC LIMIT 5")
    patients = cur.fetchall()
    con.close()
    return patients

def getRecentPredictions(patient_id):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("select * from patientPredictions where patientid = %s", patient_id)
    recent_predictions = cur.fetchall()
    con.close()
    return recent_predictions
	
def insertPrediction(patient_id, file_location, prediction_result):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("INSERT INTO patientPredictions (patientid,prediction_data_location,prediction_result) VALUES (%s,%s,%s)",
            (patient_id,file_location,prediction_result))
    con.commit()
    con.close()
    success = 1
    return success	

def removePatient(patient_id):
    con = pymysql.connect(host="35.184.27.214", user='root', password='whabidb', db='whabi')
    cur = con.cursor()
    cur.execute("DELETE FROM patients WHERE patientid = %s", (patient_id))
    con.commit()
    con.close()
    success = 1
    return success	
	
	
	
	
	
	
