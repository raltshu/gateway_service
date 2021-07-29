import os, json, logging
from flask_classful import FlaskView, route
from flask import request,render_template
import requests

fitservice = os.environ['fitservice_endpoint']


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

        return render_template('predict/predict_result.html' ,predicted_price=response.text, data=row)


