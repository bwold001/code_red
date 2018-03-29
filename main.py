#%env KERAS_BACKEND=tensorflow
import keras
from keras.models import model_from_json
import pandas as pd
import h5py
import request
#import MySQLdb

from google.cloud import datastore
from google.cloud import storage
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://id2528699_whabi:whabi.99.000webhost.io/id2528699_patient_info'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#db = SQLAlchemy(app)
#class test(db.Model):
#    fname=db.Column(db.Integer(11))
#    lname=db.Column(db.Integer(11))

#db = MySQLdb.connect(host='48557.us-imm-sql6.000webhost.io', user='id2528699_whabi', passwd='whabi', db='id2528699_patient_info', port=3306)
#cur = db.cursor()

def getPrediction(patient_features):
    model = model_from_json(open('model/model_100.json').read())
    model.load_weights('model/model_100.h5')
    # features.csv should be a csv file with columns in the order
    # described in features_100.txt, features_500.txt, or features_full.txt.

    patients = pd.read_csv(patient_features, index_col=0)
    #print (patients)

    predictions = model.predict_proba(patients.values)[:, 0]
    pred_percent = int(predictions[0]*100)
    return pred_percent


@app.route('/')
def homepage():
    # Create a Cloud Datastore client.
    #datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    #query = datastore_client.query(kind='Faces')
	    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template ('main.html')  #, image_entities=image_entities)
    #pred = getPrediction('features/features.csv')
    #print(pred)

@app.route('/insert_features', methods=['GET','POST'])
def insert_features():
    fname = request.form['fname']
    lname = request.form['lname']
    #sig = test(fname=fname, lname=lname)
    #db.session.add(sig)
    #db.session.commit()
    #cur.execute('''INSERT INTO test (fname, lname) VALUES (%s,%s)''',(lname, fname))
	#prediction = getPrediction(features/features.csv)
    return fname,lname

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=9090, debug=True)