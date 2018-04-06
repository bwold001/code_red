
from flask import Flask, request, redirect, render_template
import models as dbHandler

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def main():
	if request.method == 'POST':
		if request.form.get('sign_up') == 'sign_up':
			return render_template('sign_up.html')
		elif request.form.get('sign_in')=='sign_in':
			return render_template('sign_in.html')
	return render_template('main.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('main.html')
		elif request.form.get('sign_up') == 'sign_up':
			email = request.form['email']
			password = request.form['password']
			fname = request.form['fname']
			lname = request.form['lname']
			phone = str(request.form['phone_number'])
			confirm_password = request.form['confirm_password']
			if password == confirm_password:
				insertUser = dbHandler.insertUser(email, password,fname,lname,phone)
				if insertUser == 1:
					return render_template('main.html',success=1)
				else:
					return render_template('sign_up.html', exist=1)
			else:
				return render_template('sign_up.html',nomatch=1)			
    else:
		return render_template('sign_up.html')
		
@app.route('/sign_in', methods=['POST','GET'])
def sign_in():
    if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('main.html')
		elif request.form.get('sign_in') == 'sign_in':
			email = request.form['email']
			password = request.form['password']
			result = dbHandler.getPassword(email)
			correct_password = str(result[0][0])
			fname = str(result[0][1])			
			if password == correct_password:
				return render_template('home.html', user_name=fname)
			else:
				return render_template('sign_in.html',wrong_pass=1)
    else:
		return render_template('sign_in.html')
		
@app.route('/home', methods=['POST','GET'])
def home():
    if request.form.get('create_patient') == 'create_patient':
	    return render_template('create_patient.html')
    elif request.form.get('search_patient') == 'search_patient':
	    return render_template('search_patient.html')
    elif request.form.get('patient_prediction') == 'patient_prediction':
        return render_template('patient_prediction.html')
    else:
        return render_template('home.html')

@app.route('/create_patient', methods=['POST', 'GET'])
def create_patient():
    if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('home.html')
		elif request.form.get('create_patient') == 'create_patient':
			fname = request.form['fname']
			lname = request.form['lname']
			email = request.form['email']
			gender = request.form['gender']
			age = str(request.form['age'])
			phone = str(request.form['phone_number'])
			race = str(request.form['race'])
			insertPatient = dbHandler.insertPatient(fname,lname,email,gender,age,phone,race)
			if insertPatient == 1:
				return render_template('home.html',success=1)
			else:
				return render_template('create_patient.html', exist=1)						
    else:
		return render_template('create_patient.html')
		
@app.route('/search_patient', methods=['POST', 'GET'])
def search_patient():
	if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('home.html')
		elif request.form.get('search_patient') == 'search_patient':
			fname = request.form['fname']
			patient_info = dbHandler.getPatientInfo(fname)
			if len(patient_info) != 0:
				patient_id = patient_info[0][0]
				lname = patient_info[0][2]
				email = patient_info[0][3]
				gender = patient_info[0][4]
				age = patient_info[0][5]
				phone = patient_info[0][6]
				race = patient_info[0][7]
				time_created = patient_info[0][8]
				return render_template('display_patient.html', patient_id=patient_id, fname=fname,
										lname=lname, email=email, gender=gender, age=age,
										phone=phone, race=race, time_created=time_created)
			else:
				return render_template('search_patient.html', noexist=1)
	else:
		return render_template('search_patient.html')
		
@app.route('/update_patient', methods=['POST', 'GET'])
def update_patient():
    if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('search_patient.html')
		elif request.form.get('update_patient') == 'update_patient':
			fname = request.form['fname']
			lname = request.form['lname']
			gender = request.form['gender']
			age = str(request.form['age'])
			phone = str(request.form['phone_number'])
			race = str(request.form['race'])
			insertPatient = dbHandler.UpdatePatient(fname,lname,gender,age,phone,race)
			if insertPatient == 1:
				return render_template('display_patient.html',success=1)
			else:
				return render_template('display_patient.html', error=1)						
    else:
		return render_template('display_patient.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')


