
from flask import Flask, request, redirect, render_template
import models as dbHandler
import csv


app = Flask(__name__)
global patient_values
patient_values = {}

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
			user_id = str(result[0][2])
			global usr_name, usr_id
			usr_name = fname
			usr_id = user_id
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
		recents = dbHandler.getRecents()
		return render_template('search_patient.html',recents=recents)
	elif request.form.get('patient_prediction') == 'patient_prediction':
		recents = dbHandler.getRecents()
		return render_template('select_patient.html', recents=recents)
	else:
		return render_template('home.html')

@app.route('/create_patient', methods=['POST', 'GET'])
def create_patient():
	if request.method=='POST':
		if request.form.get('back') == 'back':
			return render_template('home.html', user_name=usr_name)
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
	recents = dbHandler.getRecents()	
	if request.method=='POST':		
		#return (str(recents))
		if request.form.get('back') == 'back':
		    return render_template('home.html',  user_name=usr_name, recents=recents)
		elif request.form.get('search_patient') == 'search_patient':						
			email = request.form['email']
			patient_info = dbHandler.getPatientInfo(email)
			if len(patient_info) == 1:
				patient_id = patient_info[0][0]
				fname = patient_info[0][1]
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
			elif len(patient_info) > 1:
				return render_template('search_patient.html', patient_info=patient_info, recents=recents)
			else:
				return render_template('search_patient.html', noexist=1, recents=recents)
		return render_template('search_patient.html', recents=recents)
		# elif request.form.get('select_patient') == 'select_patient':
			# p_id = request.form['p_id']
			# patient_info = dbHandler.getPatientInfoByID(p_id)
			# if len(patient_info) == 1:
				# patient_id = patient_info[0][0]
				# lname = patient_info[0][2]
				# email = patient_info[0][3]
				# gender = patient_info[0][4]
				# age = patient_info[0][5]
				# phone = patient_info[0][6]
				# race = patient_info[0][7]
				# time_created = patient_info[0][8]
			# return render_template('display_patient.html', patient_id=patient_id, fname=fname,
										# lname=lname, email=email, gender=gender, age=age,
										# phone=phone, race=race, time_created=time_created)
	else:
	
		return render_template('search_patient.html',recents=recents)
		
@app.route('/update_patient', methods=['POST', 'GET'])
def update_patient():
	if request.method=='POST':
		if request.form.get('back') == 'back':
			return render_template('search_patient.html', recents=recents)
		elif request.form.get('update_patient') == 'update_patient':
			patient_id = request.form['patient_id']
			fname = request.form['fname']
			lname = request.form['lname']
			gender = request.form['gender']
			phone = str(request.form['phone_number'])
			race = str(request.form['race'])
			updatePatient = dbHandler.updatePatient(patient_id,fname,lname,gender,phone,race)
			if updatePatient == 1:
				return render_template('display_patient.html',success=1)
			else:
				return render_template('display_patient.html', error=1)						
	else:
		return render_template('display_patient.html')

@app.route('/select_patient', methods=['POST', 'GET'])
def select_patient():
	recents = dbHandler.getRecents()	
	if request.method=='POST':
		if request.form.get('back') == 'back':
		    return render_template('home.html',  user_name=usr_name, recents=recents)
		elif request.form.get('select_patient') == 'select_patient':						
			email = request.form['email']
			patient_info = dbHandler.getPatientInfo(email)
			if len(patient_info) == 1:
				patient_id = patient_info[0][0]
				fname = patient_info[0][1]
				lname = patient_info[0][2]
				email = patient_info[0][3]
				gender = patient_info[0][4]
				age = patient_info[0][5]
				phone = patient_info[0][6]
				race = patient_info[0][7]
				time_created = patient_info[0][8]
				return render_template('prediction_form.html', patient_id=patient_id, fname=fname,
										lname=lname, email=email, gender=gender, age=age,
										phone=phone, race=race, time_created=time_created)
			elif len(patient_info) > 1:
				return render_template('select_patient.html', patient_info=patient_info, recents=recents)
			else:
				return render_template('select_patient.html', noexist=1, recents=recents)
		return render_template('select_patient.html', recents=recents)
	else:	
		return render_template('select_patient.html',recents=recents)
		
@app.route('/get_prediction', methods=['POST', 'GET'])
def get_prediction():
	if request.method=='POST':
		
		patient_id = request.form['patient_id']
		fname = request.form['fname']
		lname = request.form['lname']
		gender = request.form['gender']
		age = str(request.form['age'])
		martial_status = request.form['martial_status']	
		admission_type = request.form['admission_type']
		breathing_problems = request.form['breathing_problems']	
		patient_uses = request.form['patient_uses']
		insurance = request.form['insurance']
		
		three_month_inpatient = str(request.form['three_month_inpatient'])
		six_month_inpatient = str(request.form['six_month_inpatient'])
		twelve_month_inpatient = str(request.form['twelve_month_inpatient'])
		three_month_emergency = str(request.form['three_month_emergency'])
		six_month_emergency = str(request.form['six_month_emergency'])
		twelve_month_emergency = str(request.form['twelve_month_emergency'])
		
			
		patient_values['BasicDemographicsExtractor__age']=age
		patient_values['BasicDemographicsExtractor__age^2']= str(int(age)**2)
		if int(age)>45:
			t_age = int(age)-45
		else:
			t_age = 0
		patient_values['BasicDemographicsExtractor__tabak_age']=str(t_age)
		patient_values['BasicDemographicsExtractor__age^3']= str(int(age)**3)
		if martial_status == 'married':
			patient_values['BasicDemographicsExtractor__marital_status_cat_married']= '1'
			patient_values['BasicDemographicsExtractor__marital_status_cat_widowed']= '0'
		elif martial_status == 'widowed':
			patient_values['BasicDemographicsExtractor__marital_status_cat_married']='0'
			patient_values['BasicDemographicsExtractor__marital_status_cat_widowed']='1'
		if gender == 'female':
			 patient_values['BasicDemographicsExtractor__if_female_bool'] = '1'
		elif gender == 'male':
			patient_values['BasicDemographicsExtractor__if_female_bool'] = '0'
			
		
		with open('static/test.csv','wb') as f:
			fieldnames = ['UtilizationExtractor__pre_6_month_inpatient','UtilizationExtractor__pre_12_month_inpatient','ComorbiditiesExtractor__charlson_index',
			'ComorbiditiesExtractor__charlson_index_lace','UtilizationExtractor__pre_3_month_inpatient','LabResultsExtractor__num_abnormal_results',
			'LabResultsExtractor__num_total_results','LabResultsExtractor__tabak_lab_score','ComorbiditiesExtractor__comor_ren','ComorbiditiesExtractor__comor_chf',
			'UtilizationExtractor__er_visits_lace','MedicationsExtractor__inp_num_unique_meds','HospitalProblemsExtractor__hospital_problems_count',
			'ProviderExtractor__specialty_obstetrics_gynecology','MedicationsExtractor__inp_num_meds','UtilizationExtractor__pre_6_month_emergency',
			'AdmissionExtractor__admission_type_cat_elective','UtilizationExtractor__pre_12_month_emergency','ComorbiditiesExtractor__comor_cpd,UtilizationExtractor__pre_3_month_emergency',
			'ProviderExtractor__specialty_hospitalist_medical','BasicDemographicsExtractor__age','DischargeExtractor__disch_location_cat_home_no_service','ProceduresExtractor__px_ot_asst_del',
			'LabResultsExtractor__tabak_very_low_albumin','BasicDemographicsExtractor__age^2','HospitalProblemsExtractor__hcup_category_chr_kidney_disease','AdmissionExtractor__acuity_lace',
			'AdmissionExtractor__admission_type_cat_emergency','ComorbiditiesExtractor__comor_mdm','MedicationsExtractor__inp_med_diuretics','DischargeExtractor__length_of_stay_lace',
			'BasicDemographicsExtractor__tabak_age','MedicationsExtractor__inp_med_minerals_&_electrolytes','BasicDemographicsExtractor__age^3','ComorbiditiesExtractor__comor_sdm',
			'HospitalProblemsExtractor__hcup_category_nml_preg_del','EncounterReasonExtractor__problem_breathing','LabResultsExtractor__tabak_high_pt_inr',
			'HospitalProblemsExtractor__hcup_category_chf_nonhp','ProviderExtractor__specialty_internal_medicine','LabResultsExtractor__pct_abnormal_results','ProceduresExtractor__px_hemodialysis',
			'ProceduresExtractor__px_ob_lacerat','ComorbiditiesExtractor__comor_mal','ProceduresExtractor__px_blood_transf','MedicationsExtractor__inp_med_antiasthmatic',
			'PayerExtractor__insurance_type_cat_medicare','HospitalProblemsExtractor__hcup_category_copd','LabResultsExtractor__tabak_high_bun','ComorbiditiesExtractor__comor_mld',
			'MedicationsExtractor__inp_med_corticosteroids','DischargeExtractor__disch_location_cat_home_health','MedicationsExtractor__inp_med_anticoagulants','ComorbiditiesExtractor__comor_mst',
			'MedicationsExtractor__inp_med_misc._antiinfectives','DischargeExtractor__disch_location_cat_snf','MedicationsExtractor__inp_med_antidiabetic',
			'MedicationsExtractor__inp_med_assorted_classes','LabResultsExtractor__hosp_low_sodium','HospitalProblemsExtractor__hcup_category_fluid_elc_dx','HospitalProblemsExtractor__hcup_category_anemia',
			'ComorbiditiesExtractor__comor_pvr','ComorbiditiesExtractor__comor_mi','HospitalProblemsExtractor__hcup_category_diabmel_w_cm','LabResultsExtractor__tabak_abnormal_sodium',
			'ProceduresExtractor__px_c_section','MedicationsExtractor__inp_med_hematopoietic_agents','DischargeExtractor__length_of_stay','ComorbiditiesExtractor__comor_sld',
			'MedicationsExtractor__outp_med_anti-rheumatic','PayerExtractor__insurance_type_cat_commercial','HospitalProblemsExtractor__hcup_category_dysrhythmia','LabResultsExtractor__tabak_very_high_bun',
			'ProceduresExtractor__px_ot_vasc_cath','LabResultsExtractor__hosp_low_hemoglobin','HospitalProblemsExtractor__hcup_category_ac_renl_fail','LabResultsExtractor__tabak_high_bilirubin',
			'VitalsExtractor__pulse','HealthHistoryExtractor__tobacco_cat_quit','HospitalProblemsExtractor__hcup_category_htn','BasicDemographicsExtractor__marital_status_cat_married',
			'MedicationsExtractor__inp_med_nutrients','MedicationsExtractor__inp_dea_class_C-II','MedicationsExtractor__inp_med_fluoroquinolones','MedicationsExtractor__inp_med_analgesics-narcotic',
			'HospitalProblemsExtractor__hcup_category_adlt_resp_fl','HospitalProblemsExtractor__hcup_category_oth_liver_dx','HealthHistoryExtractor__alcohol_cat_no',
			'LabResultsExtractor__tabak_high_troponin_or_ckmb','LabResultsExtractor__tabak_low_albumin','ProceduresExtractor__px_ca_chemorx','BasicDemographicsExtractor__marital_status_cat_widowed',
			'HospitalProblemsExtractor__hcup_category_ot_compl_bir','LabResultsExtractor__tabak_abnormal_pco2','DischargeExtractor__disch_time_cat_morning','HospitalProblemsExtractor__hcup_category_oth_low_resp',
			'BasicDemographicsExtractor__if_female_bool','HospitalProblemsExtractor__hcup_category_septicemia','HospitalProblemsExtractor__hcup_category_diabmel_no_c']

			writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=',', quotechar='|')
			writer.writeheader()
			writer.writerow({'UtilizationExtractor__pre_6_month_inpatient': age})
				
		prediction_result = 9
		return render_template("prediction_result.html", prediction_result=prediction_result)
	else:
		return render_template('prediction_form.html')		

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')


