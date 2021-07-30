import os, json, logging
from flask_classful import FlaskView, route
from flask import request,render_template
import requests

fitservice = os.environ['fitservice_endpoint']
dataservice = os.environ['dataservice_endpoint']


class PredictView(FlaskView):

    @route('/', methods=['GET'])
    def index(self):
        response = requests.get(url=f"{fitservice}/fit/status")
        if response.status_code == 200:
            model_state = json.loads(response.text)
        return render_template('predict/predict.html',state=model_state)
    
    @route('/', methods=['POST'])
    def submit_prediction(self):
        row = {
            'carat':request.form["carat"],
            'depth':request.form["depth"],
            'table':request.form["table"],
            'cut':request.form["cut"],
            'color':request.form["color"],
            'clarity':request.form["clarity"],
            'x':request.form["x"],
            'y':request.form["y"],
            'z':request.form["z"]
        }
        response = requests.post(url=f"{fitservice}/fit/predict", json=row) 
        row['predicted_price'] = float(response.text)
        audit_response = requests.post(url=f"{dataservice}/data/audit", json=row)

        return render_template('predict/predict_result.html' ,predicted_price=float(response.text), data=row, row_id=int(audit_response.text))

    @route('/feedback/<int:row_id>', methods=['POST','PUT'])
    def user_feedback(self, row_id):
        grade = request.form['grade']
        user_prediction = request.form['user_prediction']
        data = {'grade':grade,'user_prediction':user_prediction}
        response = requests.put(url=f"{dataservice}/data/feedback/{row_id}", json=data)

        return render_template('predict/feedback_thank_you.html')


