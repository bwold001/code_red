import os
import unittest
 
from application import app

class BasicTests(unittest.TestCase):
  
    # executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
 
    # executed after each test
	def tearDown(self):
		pass

	#tests
	def test_main_page(self):
		response = self.app.get('/', context_type='html/text')
		self.assertEqual(response.status_code, 200)
		
	def sign_up(self):
		response = self.app.post('/sign_up', data=dict(fname="test",lname="user",email="test_user@gmail.com", phone_number="3144565454", password="test", confirm="test"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Successfully Registered',  response.data)

	def sign_up_diff_pass(self):
		response = self.app.post('/sign_up', data=dict(fname="test",lname="user",email="test_user@gmail", phone_number="3144565454",password="test", confirm="nottest"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Passwords Donot Match',  response.data)
	
	def sign_up_existing_email(self):
		response = self.app.post('/sign_up', data=dict(fname="test",lname="user",email="bwold@gmail.com", phone_number="3144565454", password="pass", confirm="pass"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Email Already Exists',  response.data)
		
	def sign_in(self):
		response = self.app.post('/sign_in', data=dict(email="bwold@gmail.com", password="pass"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Successfully Signed In',  response.data)
	
	def sign_in_wrong_pass(self):
		response = self.app.post('/sign_in', data=dict(email="bwold@gmail.com", password="wrongpass"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Incorrect_password',  response.data)

	def sign_in_wrong_email(self):
		response = self.app.post('/sign_in', data=dict(email="noexist@gmail.com", password="pass"), follow_redirects=True)
		self.assertEqual(response.status_code, 200) 
		self.assertIn('Email Does not Exist',  response.data)

	def update_profile(self):
		with self.client:
			self.client.post('/sign_in', data=dict(fname="test_two",lname="user_two",email="bwold@gmail.com", phone_number="35656241414", password="passw", confirm="passw"),follow_redirects=True)
			response = self.client.post('/update_profile', data=dict(fname="test",lname="test", email="test@gmail.com",gender="female",race="Black"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('Patient Successfully Created',  response.data)
		
	def create_patient(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/create_patient', data=dict(fname="test",lname="test", email="test@gmail.com",age="22", phone_number="3144565454", gender="female",race="Black"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('Patient Successfully Created',  response.data)
	
	def create_patient_existing_email(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/create_patient', data=dict(fname="test",lname="test", email="test@gmail.com",gender="female", age="22", phone_number="3144565454", race="Black"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('A Patient With That Email Exists.',  response.data)
	
	def update_patient(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/update_patient', data=dict(fname="test2",lname="test2", email="test@gmail.com",gender="female",race="Black"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('Patient Successfully Created',  response.data)
			
	def display_patient(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/display_patient', data=dict(fname="test",lname="test", email="test",gender="female", age="22", phone_number="3144565454",race="White"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)

	def search_exist_patient(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/search_patient', data=dict(email="awest@gmail.com"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			
	def search_no_exist_patient(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/search_patient', data=dict(email="noexist@gmail.com"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			self.assertIn('No Patient Found With That Email',  response.data)

	def prediction_form(self):
		with self.client:
			self.client.post('/sign_in', data=dict(username="bwold@gmail.com", password="passw"),follow_redirects=True)
			response = self.client.post('/display_patient', data=dict(fname="test",lname="test", gender="female", age="22", marial_status="Married", admission_type="elective", insurance="medicare", 
						three_month_inpatient="2",six_month_inpatient="5",twelve_month_inpatient="5",three_month_emergency="5",six_month_emergency="5",twelve_month_emergency="5",hospital_problems_count="5",pulse="5",
						num_total_lab_results="5", num_abnormal_results="5",tabak_lab_score="5", tabak_very_low_albumin="5",tabak_high_pt_inr="5", tabak_high_bun="5",
						hosp_low_sodium="5", hosp_low_hemoglobin="5",tabak_high_bilirubin="5", tabak_high_troponin="5",tabak_high_troponin_ckmb="5",tabak_low_albumin="5",
						tabak_abnormal_pco2="5",charlson_index="5",inp_num_meds="5",inp_num_unique_meds="5",length_of_stay="5",	disch_time="disch_time_cat_morning",
						disch_location="disch_location_cat_home_health"), follow_redirects=True)
			self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main() 