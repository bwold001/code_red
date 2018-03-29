<?php

$host="99.000webhost.com";
$port=3306;
$socket="";
$user="id2528699_whabi";
$password="whabi";
$dbname="id2528699_patient_info";

#$first_name = $_POST['first_name'];
#$last_name = $_POST['last_name'];
#$gender = $_POST['gender'];
#$email = $_POST['email'];
#$qualification = $_POST['qualification'];
#$password = $_POST['confirm_password'];

//if ($_POST['terms_conditions'] == 'checked'){
//	$terms_conditions = 'accepted';
//}

//create and check connection
$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
	or die ('Could not connect to the database server' . mysqli_connect_error());


				
$feature_set_1 = "INSERT INTO feature_set_1(`UtilizationExtractor__pre_6_month_inpatient`, `UtilizationExtractor__pre_12_month_inpatient`, `ComorbiditiesExtractor__charlson_index`, 
			`ComorbiditiesExtractor__charlson_index_lace`, `UtilizationExtractor__pre_3_month_inpatient`, `LabResultsExtractor__num_abnormal_results`, 
			`LabResultsExtractor__num_total_results`, `LabResultsExtractor__tabak_lab_score`, `ComorbiditiesExtractor__comor_ren`, `ComorbiditiesExtractor__comor_chf`, 
			`UtilizationExtractor__er_visits_lace`, `MedicationsExtractor__inp_num_unique_meds`, `HospitalProblemsExtractor__hospital_problems_count`, 
			`ProviderExtractor__specialty_obstetrics_gynecology`, `MedicationsExtractor__inp_num_meds`, `UtilizationExtractor__pre_6_month_emergency`, 
			`AdmissionExtractor__admission_type_cat_elective`, `UtilizationExtractor__pre_12_month_emergency`, `ComorbiditiesExtractor__comor_cpd`, 
			`UtilizationExtractor__pre_3_month_emergency`, `ProviderExtractor__specialty_hospitalist_medical`, `BasicDemographicsExtractor__age`, 
			`DischargeExtractor__disch_location_cat_home_no_service`, `ProceduresExtractor__px_ot_asst_del`, `LabResultsExtractor__tabak_very_low_albumin`) 
			
		VALUES ('0','0','0','0', '0','0','0','0','0','0'
				'0','0','0','0', '0','0','0','0','0', '0'
				'0','0','0','0', '0')";

$feature_set_2 = "INSERT INTO `feature_set_2`(`HospitalProblemsExtractor__hcup_category_chr_kidney_disease`, `AdmissionExtractor__acuity_lace`, 
				`AdmissionExtractor__admission_type_cat_emergency`, `ComorbiditiesExtractor__comor_mdm`, `MedicationsExtractor__inp_med_diuretics`, `DischargeExtractor__length_of_stay_lace`,
				`BasicDemographicsExtractor__tabak_age`, `MedicationsExtractor__inp_med_minerals_&_electrolytes`, `BasicDemographicsExtractor__age^3`, `ComorbiditiesExtractor__comor_sdm`, 
				`HospitalProblemsExtractor__hcup_category_nml_preg_del`, `EncounterReasonExtractor__problem,_breathing`, `LabResultsExtractor__tabak_high_pt_inr`, 
				`HospitalProblemsExtractor__hcup_category_chf_nonhp`, `ProviderExtractor__specialty_internal_medicine`, `LabResultsExtractor__pct_abnormal_results`, 
				`ProceduresExtractor__px_hemodialysis`, `ProceduresExtractor__px_ob_lacerat`, `ComorbiditiesExtractor__comor_mal`, `ProceduresExtractor__px_blood_transf`, 
				`MedicationsExtractor__inp_med_antiasthmatic`, `PayerExtractor__insurance_type_cat_medicare`, `HospitalProblemsExtractor__hcup_category_copd`, `LabResultsExtractor__tabak_high_bun`, 
				`ComorbiditiesExtractor__comor_mld`) 
				
			VALUES '0','0','0','0', '0','0','0','0','0','0'
				'0','0','0','0', '0','0','0','0','0', '0'
				'0','0','0','0', '0')";
				
$feature_set_3 = "insert into feature_set_3 (MedicationsExtractor__inp_med_corticosteroids, DischargeExtractor__disch_location_cat_home_health, 
			MedicationsExtractor__inp_med_anticoagulants, ComorbiditiesExtractor__comor_mst, MedicationsExtractor__inp_med_misc._antiinfectives, 
			DischargeExtractor__disch_location_cat_snf, MedicationsExtractor__inp_med_antidiabetic, MedicationsExtractor__inp_med_assorted_classes, 
			LabResultsExtractor__hosp_low_sodium, HospitalProblemsExtractor__hcup_category_fluid_elc_dx, HospitalProblemsExtractor__hcup_category_anemia, 
			ComorbiditiesExtractor__comor_pvr, ComorbiditiesExtractor__comor_mi, HospitalProblemsExtractor__hcup_category_diabmel_w_cm, 
			LabResultsExtractor__tabak_abnormal_sodium, ProceduresExtractor__px_c_section, MedicationsExtractor__inp_med_hematopoietic_agents, 
			DischargeExtractor__length_of_stay, ComorbiditiesExtractor__comor_sld, MedicationsExtractor__outp_med_anti-rheumatic, 
			PayerExtractor__insurance_type_cat_commercial, HospitalProblemsExtractor__hcup_category_dysrhythmia, LabResultsExtractor__tabak_very_high_bun, 
			ProceduresExtractor__px_ot_vasc_cath, LabResultsExtractor__hosp_low_hemoglobin)
					
		values ('0','0','0','0', '0','0','0','0','0','0'
				'0','0','0','0', '0','0','0','0','0', '0'
				'0','0','0','0', '0')";

#$pass = "insert into students_login(pass) values ($password)";


//mysqli_query($con,$sql)or die (mysqli_error($con));;
if ($con->query($sql)===TRUE) {
	 echo "Student Successfully Added.";
 } else { "Error:" . $sql. $con->error;}
 


?>