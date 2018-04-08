import keras
from keras.models import model_from_json
import pandas as pd
import h5py

def getPrediction(patient_features):
    model = model_from_json(open('model/model_100.json').read())
    model.load_weights('model/model_100.h5')

    # features.csv should be a csv file with columns in the order
    # described in features_full.txt.

    patients = pd.read_csv(patient_features)
    #print(patients.shape[1])
    #print (patients)
    predictions = model.predict_proba(patients.values)[:, 0]
    pred_percent = int(predictions[0]*100)
    return pred_percent

#pred = getPrediction('static/Samuel20180407-230146prediction_data.csv')
#print(pred)