
from flask import Flask, request, redirect, render_template
import db_models as dbHandler
import csv
from collections import OrderedDict
import time
import prediction_model

app = Flask(__name__)
global patient_values
patient_values = OrderedDict()

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
			#return (str(result))
			if len(result) == 0:
				return render_template('sign_in.html',no_exist=1)
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
		global recents
		recents = dbHandler.getRecents()
		return render_template('search_patient.html',recents=recents)
	elif request.form.get('patient_prediction') == 'patient_prediction':
		recents = dbHandler.getRecents()
		return render_template('select_patient.html', recents=recents)
	elif request.form.get('edit') == 'edit':
		user_info = dbHandler.getUserInfo(usr_id)
		user_id = user_info[0][0]
		fname = user_info[0][3]
		lname = user_info[0][4]
		email = user_info[0][1]
		phone = user_info[0][5]
		time_created = user_info[0][6]
		return (fname)
		#return render_template('edit_profile.html', user_id=user_id, fname=fname,
		#					lname=lname, email=email, phone=phone, time_created=time_created)
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
	#else:
	#	return render_template('create_patient.html')
		
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
				recent_predictions = dbHandler.getRecentPredictions(patient_id)
				return render_template('display_patient.html', patient_id=patient_id, fname=fname,
										lname=lname, email=email, gender=gender, age=age,
										phone=phone, race=race, time_created=time_created, recent_predictions = recent_predictions)
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
	#else:
	#	return render_template('search_patient.html')
		
@app.route('/update_patient', methods=['POST', 'GET'])
def update_patient():
	recents = dbHandler.getRecents()
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
		elif request.form.get('remove_patient')== 'remove_patient':
			patient_id = request.form['patient_id']
			remove_patient = dbHandler.removePatient(patient_id)
			if remove_patient == 1:
				return render_template ('search_patient.html', removed=1, recents=recents)
			else:
				return render_template ('search_patient.html', notremoved=1)
	#else:
	#	return render_template('display_patient.html')

@app.route('/update_profile', methods=['POST', 'GET'])
def update_profile():
	if request.method=='POST':		
		if request.form.get('back') == 'back':
			return render_template('home.html', user_name=usr_name)
		elif request.form.get('update_profile') == 'update_profile':
			fname = request.form['fname']
			lname = request.form['lname']
			email = request.form['email']
			phone = str(request.form['phone_number'])
			password = request.form['password']
			confirm_update_password = request.form['confirm_update_password']
			if not password and not confirm_update_password:
				success = dbHandler.updateUserProfile(usr_id,fname,lname,phone,password)
				return render_template('home.html',updated=1)
			elif password == confirm_update_password:
				success = dbHandler.updateUserProfile(usr_id,fname,lname,phone,password)
				return render_template('home.html',updated=1)
			else:
				return render_template ('edit_profile.html', nomatch=1)
								
	else:
		user_info = dbHandler.getUserInfo(usr_id)
		user_id = user_info[0][0]
		fname = user_info[0][3]
		lname = user_info[0][4]
		email = user_info[0][1]
		phone = user_info[0][5]
		time_created = user_info[0][6]
		return render_template('edit_profile.html', user_id=user_id, fname=fname,
							lname=lname, email=email, phone=phone, time_created=time_created)
		#return render_template('edit_profile.html', user_id=usr_id)

		
		
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
				global patient_name
				patient_name=lname
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
	#else:	
	#	return render_template('select_patient.html',recents=recents)
		
@app.route('/get_prediction', methods=['POST', 'GET'])
def get_prediction():
	if request.method=='POST':
		#first tab in form
		global patient_id, lname
		patient_id = request.form['patient_id']
		fname = request.form['fname']
		lname = request.form['lname']
		gender = request.form['gender']
		age = str(request.form['age'])
		martial_status = request.form['martial_status']	
		
		if int(age)>45:
				t_age = int(age)-45
		else:
			t_age = 0		
		patient_values['BasicDemographicsExtractor__tabak_age']=str(t_age)
		patient_values['BasicDemographicsExtractor__age']=age
		patient_values['BasicDemographicsExtractor__age^2']= str(int(age)**2)
		patient_values['BasicDemographicsExtractor__age^3']=str(int(age)**3)		
		if martial_status == 'married':
			patient_values['BasicDemographicsExtractor__marital_status_cat_married']= 1
			patient_values['BasicDemographicsExtractor__marital_status_cat_widowed']= 0
		elif martial_status == 'widowed':
			patient_values['BasicDemographicsExtractor__marital_status_cat_married']=0
			patient_values['BasicDemographicsExtractor__marital_status_cat_widowed']=1
		elif martial_status == 'neither':
			patient_values['BasicDemographicsExtractor__marital_status_cat_married']=0
			patient_values['BasicDemographicsExtractor__marital_status_cat_widowed']=0
		if gender == 'female':
			patient_values['BasicDemographicsExtractor__if_female_bool'] = 1
		elif gender == 'male':
			patient_values['BasicDemographicsExtractor__if_female_bool'] = 0
		
		
		#second tab in form
		admission_type = request.form['admission_type']
		breathing_problems = request.form.getlist('breathing_problems')	
		patient_uses = request.form.getlist('patient_uses')
		insurance = request.form['insurance']
		three_month_inpatient = str(request.form['three_month_inpatient'])
		six_month_inpatient = str(request.form['six_month_inpatient'])
		twelve_month_inpatient = str(request.form['twelve_month_inpatient'])
		three_month_emergency = str(request.form['three_month_emergency'])
		six_month_emergency = str(request.form['six_month_emergency'])
		twelve_month_emergency = str(request.form['twelve_month_emergency'])
		
		if admission_type == 'elective':
			patient_values['AdmissionExtractor__admission_type_cat_elective']=1
			patient_values['AdmissionExtractor__admission_type_cat_emergency']=0
			patient_values['AdmissionExtractor__acuity_lace']=0
		elif admission_type == 'emergency':
			patient_values['AdmissionExtractor__admission_type_cat_elective']=0
			patient_values['AdmissionExtractor__admission_type_cat_emergency']=1
			patient_values['AdmissionExtractor__acuity_lace']=3			
		patient_values['EncounterReasonExtractor__problem_breathing']=0
		if len(breathing_problems) != 0:
			patient_values['EncounterReasonExtractor__problem_breathing']=1				
		if len(patient_uses) == 1:
			if patient_uses == 'tobacco':
				patient_values['HealthHistoryExtractor__tobacco_cat_quit']=0
				patient_values['HealthHistoryExtractor__alcohol_cat_no']=1
			elif patient_uses == 'alcohol':
				patient_values['HealthHistoryExtractor__tobacco_cat_quit']=1
				patient_values['HealthHistoryExtractor__alcohol_cat_no']=0
		elif len(patient_uses) == 2 :
			patient_values['HealthHistoryExtractor__tobacco_cat_quit']=0
			patient_values['HealthHistoryExtractor__alcohol_cat_no']=0
		elif len(patient_uses) == 0:
			patient_values['HealthHistoryExtractor__tobacco_cat_quit']=1
			patient_values['HealthHistoryExtractor__alcohol_cat_no']=1
		if insurance == 'medicare':
			patient_values['PayerExtractor__insurance_type_cat_medicare']=1
			patient_values['PayerExtractor__insurance_type_cat_commercial']=0
		elif insurance == 'commercial':
			patient_values['PayerExtractor__insurance_type_cat_medicare']=0
			patient_values['PayerExtractor__insurance_type_cat_commercial']=1		
		patient_values['UtilizationExtractor__pre_6_month_inpatient']=six_month_inpatient
		patient_values['UtilizationExtractor__pre_12_month_inpatient']=twelve_month_inpatient
		patient_values['UtilizationExtractor__pre_3_month_inpatient']=three_month_inpatient
		if int(six_month_emergency)< 4:
			patient_values['UtilizationExtractor__er_visits_lace']=six_month_emergency
		else:
			patient_values['UtilizationExtractor__er_visits_lace']=4
		patient_values['UtilizationExtractor__pre_6_month_emergency']=six_month_emergency
		patient_values['UtilizationExtractor__pre_12_month_emergency']=twelve_month_emergency 
		patient_values['UtilizationExtractor__pre_3_month_emergency']=three_month_emergency
		
		
		#third tab in form
		provider_speciality = request.form.getlist('speciality')
		hospital_problems_count = request.form['hospital_problems_count']
		hcup_category = request.form.getlist('hcup_category')
		
		patient_values['ProviderExtractor__specialty_obstetrics_gynecology']=0
		patient_values['ProviderExtractor__specialty_hospitalist_medical']=0
		patient_values['ProviderExtractor__specialty_internal_medicine']=0
		for speciality in provider_speciality:
			patient_values[speciality]=1		
		patient_values['HospitalProblemsExtractor__hospital_problems_count']=hospital_problems_count		
		patient_values['HospitalProblemsExtractor__hcup_category_chr_kidney_disease']=0
		patient_values['HospitalProblemsExtractor__hcup_category_nml_preg_del']=0
		patient_values['HospitalProblemsExtractor__hcup_category_chf_nonhp']=0
		patient_values['HospitalProblemsExtractor__hcup_category_copd']=0
		patient_values['HospitalProblemsExtractor__hcup_category_fluid_elc_dx']=0
		patient_values['HospitalProblemsExtractor__hcup_category_anemia']=0
		patient_values['HospitalProblemsExtractor__hcup_category_diabmel_w_cm']=0
		patient_values['HospitalProblemsExtractor__hcup_category_dysrhythmia']=0
		patient_values['HospitalProblemsExtractor__hcup_category_ac_renl_fail']=0
		patient_values['HospitalProblemsExtractor__hcup_category_htn']=0
		patient_values['HospitalProblemsExtractor__hcup_category_adlt_resp_fl']=0
		patient_values['HospitalProblemsExtractor__hcup_category_oth_liver_dx']=0
		patient_values['HospitalProblemsExtractor__hcup_category_ot_compl_bir']=0
		patient_values['HospitalProblemsExtractor__hcup_category_oth_low_resp']=0
		patient_values['HospitalProblemsExtractor__hcup_category_septicemia']=0
		patient_values['HospitalProblemsExtractor__hcup_category_diabmel_no_c']=0
		for problem in hcup_category:
			patient_values[problem]=1
		
		#fourth tab in form
		ccs_category = request.form.getlist('ccs_category')
		pulse = request.form['pulse']
		num_total_lab_results = request.form['num_total_lab_results']
		num_abnormal_results = request.form['num_abnormal_results']
		tabak_lab_score = request.form['tabak_lab_score']
		
		tabak_very_low_albumin = request.form['tabak_very_low_albumin']
		tabak_high_pt_inr = request.form['tabak_high_pt_inr']
		tabak_high_bun = request.form['tabak_high_bun']
		hosp_low_sodium = request.form['hosp_low_sodium']
		hosp_low_hemoglobin = request.form['hosp_low_hemoglobin']
		tabak_high_bilirubin = request.form['tabak_high_bilirubin']
		#tabak_high_troponin_or_ckmb = request.form['tabak_high_troponin_or_ckmb']
		tabak_high_troponin = request.form['tabak_high_troponin']		
		tabak_high_troponin_ckmb = request.form['tabak_high_troponin_ckmb']
		tabak_low_albumin = request.form['tabak_low_albumin']
		tabak_abnormal_pco2 = request.form['tabak_abnormal_pco2']
		charlson_index = request.form['charlson_index']
		comorbid = request.form.getlist('comorbid')
		
		patient_values['ProceduresExtractor__px_ot_asst_del']=0
		patient_values['ProceduresExtractor__px_hemodialysis']=0
		patient_values['ProceduresExtractor__px_ob_lacerat']=0
		patient_values['ProceduresExtractor__px_blood_transf']=0
		patient_values['ProceduresExtractor__px_c_section']=0
		patient_values['ProceduresExtractor__px_ot_vasc_cath']=0
		patient_values['ProceduresExtractor__px_ca_chemorx']=0
		for ccs in ccs_category:
			patient_values[ccs]=1
		patient_values['VitalsExtractor__pulse'] = pulse
		patient_values['LabResultsExtractor__num_abnormal_results']=num_abnormal_results
		patient_values['LabResultsExtractor__num_total_results']= num_total_lab_results
		patient_values['LabResultsExtractor__tabak_lab_score']= tabak_lab_score		
		patient_values['LabResultsExtractor__tabak_low_albumin']=0		
		patient_values['LabResultsExtractor__tabak_very_low_albumin']=0
		patient_values['LabResultsExtractor__tabak_high_pt_inr']=0
		patient_values['LabResultsExtractor__tabak_high_bun']=0
		patient_values['LabResultsExtractor__hosp_low_sodium']=0
		patient_values['LabResultsExtractor__pct_abnormal_results']= 0
		patient_values['LabResultsExtractor__tabak_abnormal_sodium']=0
		patient_values['LabResultsExtractor__tabak_very_high_bun']=0
		patient_values['LabResultsExtractor__hosp_low_hemoglobin']=0
		patient_values['LabResultsExtractor__tabak_high_bilirubin']=0
		patient_values['LabResultsExtractor__tabak_high_troponin_or_ckmb']=0
		patient_values['LabResultsExtractor__tabak_low_albumin']=0
		patient_values['LabResultsExtractor__tabak_abnormal_pco2']=0
		
		if float(tabak_very_low_albumin) <= 2.4:
					patient_values['LabResultsExtractor__tabak_very_low_albumin']=1
		if float(tabak_low_albumin) <= 2.4:
			patient_values['LabResultsExtractor__tabak_low_albumin']=1
		if float(tabak_high_pt_inr) > 1.2:	
			patient_values['LabResultsExtractor__tabak_high_pt_inr']=0
		patient_values['LabResultsExtractor__pct_abnormal_results']= (int(num_abnormal_results)/int(num_total_lab_results))*100
		if 35 <= int(tabak_high_bun) <= 50:
			patient_values['LabResultsExtractor__tabak_high_bun']=1
		if int(hosp_low_sodium) <= 135:	
			patient_values['LabResultsExtractor__hosp_low_sodium']=1
		if 131 <= int(hosp_low_sodium) < 135 or int(hosp_low_sodium) > 145:
			patient_values['LabResultsExtractor__tabak_abnormal_sodium']=1
		if 51 <= int(tabak_high_bun) <= 70:
			patient_values['LabResultsExtractor__tabak_very_high_bun']=1
		if int(hosp_low_hemoglobin) < 12:
			patient_values['LabResultsExtractor__hosp_low_hemoglobin']=1
		if float(tabak_high_bilirubin) > 1.4:
			patient_values['LabResultsExtractor__tabak_high_bilirubin']=1
		if int (tabak_high_troponin) > 1 or int(tabak_high_troponin_ckmb) > 9:
			patient_values['LabResultsExtractor__tabak_high_troponin_or_ckmb']=1
		if 2.5 <= float (tabak_low_albumin) <= 2.7:
			patient_values['LabResultsExtractor__tabak_low_albumin']=1
		if 35 <= int(tabak_abnormal_pco2) or  int(tabak_abnormal_pco2)>= 60:
			patient_values['LabResultsExtractor__tabak_abnormal_pco2']=1
		
		patient_values['ComorbiditiesExtractor__charlson_index']=charlson_index
		patient_values['ComorbiditiesExtractor__charlson_index_lace']=charlson_index
		patient_values['ComorbiditiesExtractor__comor_ren']=0
		patient_values['ComorbiditiesExtractor__comor_chf']=0
		patient_values['ComorbiditiesExtractor__comor_cpd']=0
		patient_values['ComorbiditiesExtractor__comor_mdm']=0
		patient_values['ComorbiditiesExtractor__comor_sdm']=0
		patient_values['ComorbiditiesExtractor__comor_mal']=0
		patient_values['ComorbiditiesExtractor__comor_mld']=0
		patient_values['ComorbiditiesExtractor__comor_mst']=0
		patient_values['ComorbiditiesExtractor__comor_pvr']=0
		patient_values['ComorbiditiesExtractor__comor_mi']=0
		patient_values['ComorbiditiesExtractor__comor_sld']=0
		if int(charlson_index) >=4:
			patient_values['ComorbiditiesExtractor__charlson_index_lace']=5
		for com in comorbid:
			patient_values[com]=1
			
		#fifth tab in form
		inp_num_meds = request.form['inp_num_meds']
		inp_num_unique_meds = request.form['inp_num_unique_meds']
		medications_inpatient = request.form.getlist('medications_inpatient')
		medications_outpatient = request.form.getlist('medications_outpatient')
		inp_num_unique_meds = request.form['inp_num_unique_meds']
		length_of_stay = request.form['length_of_stay']
		disch_time = request.form['disch_time']
		disch_location = request.form['disch_location']
		
		patient_values['MedicationsExtractor__inp_num_unique_meds'] = inp_num_unique_meds
		patient_values['MedicationsExtractor__inp_num_meds']= inp_num_meds
		
		patient_values['MedicationsExtractor__inp_med_diuretics']=0
		patient_values['MedicationsExtractor__inp_med_minerals_&_electrolytes']=0
		patient_values['MedicationsExtractor__inp_med_antiasthmatic']=0
		patient_values['MedicationsExtractor__inp_med_corticosteroids']=0
		patient_values['MedicationsExtractor__inp_med_anticoagulants']=0
		patient_values['MedicationsExtractor__inp_med_misc._antiinfectives']=0
		patient_values['MedicationsExtractor__inp_med_antidiabetic']=0
		patient_values['MedicationsExtractor__inp_med_assorted_classes']=0
		patient_values['MedicationsExtractor__inp_med_hematopoietic_agents']=0
		patient_values['MedicationsExtractor__outp_med_anti-rheumatic']=0
		for medication in medications_outpatient:
			patient_values[medication]=1
		
		patient_values['MedicationsExtractor__inp_med_nutrients']=0
		patient_values['MedicationsExtractor__inp_dea_class_C-II']=0
		patient_values['MedicationsExtractor__inp_med_fluoroquinolones']=0
		patient_values['MedicationsExtractor__inp_med_analgesics-narcotic']=0
		for medication in medications_inpatient:
			patient_values[medication]=1		
		if disch_location == 'disch_location_cat_snf':
			patient_values['DischargeExtractor__disch_location_cat_home_no_service']=0
			patient_values['DischargeExtractor__disch_location_cat_home_health']=0
			patient_values['DischargeExtractor__disch_location_cat_snf']=1
		elif disch_location =='disch_location_cat_home_health':
			patient_values['DischargeExtractor__disch_location_cat_home_no_service']=0
			patient_values['DischargeExtractor__disch_location_cat_home_health']=1
			patient_values['DischargeExtractor__disch_location_cat_snf']=0
		elif disch_location=='disch_location_cat_home_no_service':
			patient_values['DischargeExtractor__disch_location_cat_home_no_service']=1
			patient_values['DischargeExtractor__disch_location_cat_home_health']=0
			patient_values['DischargeExtractor__disch_location_cat_snf']=0		
		patient_values['DischargeExtractor__length_of_stay_lace']=length_of_stay
		if 4<= int(length_of_stay)<=6:
			patient_values['DischargeExtractor__length_of_stay_lace']=4
		elif 7<= int(length_of_stay)<=13:
			patient_values['DischargeExtractor__length_of_stay_lace']=5
		elif int(length_of_stay) >= 14:
			patient_values['DischargeExtractor__length_of_stay_lace']=7			
		patient_values['DischargeExtractor__length_of_stay']=length_of_stay	
		if disch_time == 'disch_time_cat_morning':
			patient_values ['DischargeExtractor__disch_time_cat_morning'] = 1
		else:
			patient_values ['DischargeExtractor__disch_time_cat_morning'] = 0	
		
		
		# with open('static/test.csv','wb') as f:
			# fieldnames = ['UtilizationExtractor__pre_6_month_inpatient','UtilizationExtractor__pre_12_month_inpatient','ComorbiditiesExtractor__charlson_index',
			# 'ComorbiditiesExtractor__charlson_index_lace','UtilizationExtractor__pre_3_month_inpatient','LabResultsExtractor__num_abnormal_results',
			# 'LabResultsExtractor__num_total_results','LabResultsExtractor__tabak_lab_score','ComorbiditiesExtractor__comor_ren','ComorbiditiesExtractor__comor_chf',
			# 'UtilizationExtractor__er_visits_lace','MedicationsExtractor__inp_num_unique_meds','HospitalProblemsExtractor__hospital_problems_count',
			# 'ProviderExtractor__specialty_obstetrics_gynecology','MedicationsExtractor__inp_num_meds','UtilizationExtractor__pre_6_month_emergency',
			# 'AdmissionExtractor__admission_type_cat_elective','UtilizationExtractor__pre_12_month_emergency','ComorbiditiesExtractor__comor_cpd,UtilizationExtractor__pre_3_month_emergency',
			# 'ProviderExtractor__specialty_hospitalist_medical','BasicDemographicsExtractor__age','DischargeExtractor__disch_location_cat_home_no_service','ProceduresExtractor__px_ot_asst_del',
			# 'LabResultsExtractor__tabak_very_low_albumin','BasicDemographicsExtractor__age^2','HospitalProblemsExtractor__hcup_category_chr_kidney_disease','AdmissionExtractor__acuity_lace',
			# 'AdmissionExtractor__admission_type_cat_emergency','ComorbiditiesExtractor__comor_mdm','MedicationsExtractor__inp_med_diuretics','DischargeExtractor__length_of_stay_lace',
			# 'BasicDemographicsExtractor__tabak_age','MedicationsExtractor__inp_med_minerals_&_electrolytes','BasicDemographicsExtractor__age^3','ComorbiditiesExtractor__comor_sdm',
			# 'HospitalProblemsExtractor__hcup_category_nml_preg_del','EncounterReasonExtractor__problem_breathing','LabResultsExtractor__tabak_high_pt_inr',
			# 'HospitalProblemsExtractor__hcup_category_chf_nonhp','ProviderExtractor__specialty_internal_medicine','LabResultsExtractor__pct_abnormal_results','ProceduresExtractor__px_hemodialysis',
			# 'ProceduresExtractor__px_ob_lacerat','ComorbiditiesExtractor__comor_mal','ProceduresExtractor__px_blood_transf','MedicationsExtractor__inp_med_antiasthmatic',
			# 'PayerExtractor__insurance_type_cat_medicare','HospitalProblemsExtractor__hcup_category_copd','LabResultsExtractor__tabak_high_bun','ComorbiditiesExtractor__comor_mld',
			# 'MedicationsExtractor__inp_med_corticosteroids','DischargeExtractor__disch_location_cat_home_health','MedicationsExtractor__inp_med_anticoagulants','ComorbiditiesExtractor__comor_mst',
			# 'MedicationsExtractor__inp_med_misc._antiinfectives','DischargeExtractor__disch_location_cat_snf','MedicationsExtractor__inp_med_antidiabetic',
			# 'MedicationsExtractor__inp_med_assorted_classes','LabResultsExtractor__hosp_low_sodium','HospitalProblemsExtractor__hcup_category_fluid_elc_dx','HospitalProblemsExtractor__hcup_category_anemia',
			# 'ComorbiditiesExtractor__comor_pvr','ComorbiditiesExtractor__comor_mi','HospitalProblemsExtractor__hcup_category_diabmel_w_cm','LabResultsExtractor__tabak_abnormal_sodium',
			# 'ProceduresExtractor__px_c_section','MedicationsExtractor__inp_med_hematopoietic_agents','DischargeExtractor__length_of_stay','ComorbiditiesExtractor__comor_sld',
			# 'MedicationsExtractor__outp_med_anti-rheumatic','PayerExtractor__insurance_type_cat_commercial','HospitalProblemsExtractor__hcup_category_dysrhythmia','LabResultsExtractor__tabak_very_high_bun',
			# 'ProceduresExtractor__px_ot_vasc_cath','LabResultsExtractor__hosp_low_hemoglobin','HospitalProblemsExtractor__hcup_category_ac_renl_fail','LabResultsExtractor__tabak_high_bilirubin',
			# 'VitalsExtractor__pulse','HealthHistoryExtractor__tobacco_cat_quit','HospitalProblemsExtractor__hcup_category_htn','BasicDemographicsExtractor__marital_status_cat_married',
			# 'MedicationsExtractor__inp_med_nutrients','MedicationsExtractor__inp_dea_class_C-II','MedicationsExtractor__inp_med_fluoroquinolones','MedicationsExtractor__inp_med_analgesics-narcotic',
			# 'HospitalProblemsExtractor__hcup_category_adlt_resp_fl','HospitalProblemsExtractor__hcup_category_oth_liver_dx','HealthHistoryExtractor__alcohol_cat_no',
			# 'LabResultsExtractor__tabak_high_troponin_or_ckmb','LabResultsExtractor__tabak_low_albumin','ProceduresExtractor__px_ca_chemorx','BasicDemographicsExtractor__marital_status_cat_widowed',
			# 'HospitalProblemsExtractor__hcup_category_ot_compl_bir','LabResultsExtractor__tabak_abnormal_pco2','DischargeExtractor__disch_time_cat_morning','HospitalProblemsExtractor__hcup_category_oth_low_resp',
			# 'BasicDemographicsExtractor__if_female_bool','HospitalProblemsExtractor__hcup_category_septicemia','HospitalProblemsExtractor__hcup_category_diabmel_no_c']

		global timestr
		timestr = time.strftime("%Y%m%d-%H%M%S")
		with open('static/'+lname+timestr+'prediction_data.csv','w',newline='') as f:
			w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			w.writerow(patient_values.keys())
			w.writerow(patient_values.values())				
			
		global prediction_result
		prediction_result = prediction_model.getPrediction('static/'+lname+timestr+'prediction_data.csv')
			
		#prediction_result = 9
		return render_template("prediction_result.html", prediction_result=str(prediction_result))
	#else:
	#	return render_template('prediction_form.html')		

		
@app.route('/save_prediction', methods=['POST', 'GET'])
def save_prediction():
	if request.method=='POST':
		upload = dbHandler.insertPrediction(patient_id, lname+timestr+'prediction_data.csv', prediction_result)		
		if upload == 1:
			return render_template ('select_patient.html', saved=1, recents=recents)
		else:
			return render_template ('select_patient.html', notsaved=1)
	#else:
	#	return render_template('prediction_result.html')
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')


