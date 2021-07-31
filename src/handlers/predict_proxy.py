import os, json, logging
from flask_classful import FlaskView, route
from flask import request,render_template
import requests
from wtforms import Form, validators, DecimalField, SelectField, StringField

fitservice = os.environ['fitservice_endpoint']
dataservice = os.environ['dataservice_endpoint']

class PredictForm(Form):
    carat = DecimalField('Carat',
        validators=[validators.required(), validators.NumberRange(min=0.0, max=3.5)], default=0.8)
    depth = DecimalField('Depth',
        validators=[validators.required(), validators.NumberRange(min=43, max=80)], default=61)
    table = DecimalField('Table',
        validators=[validators.required(), validators.NumberRange(min=43, max=100)], default=57)
    cut = SelectField('Cut', 
        choices=[('Ideal','Ideal'),('Premium','Premium'),('Very Good','Very Good'),('Good','Good'),('Fair','Fair')],
        validate_choice=True)
    color = SelectField('Color', 
        choices=[('D','D'),('E','E'),('F','F'),('G','G'),('H','H'),('I','I'),('J','J')],
        validate_choice=True)
    clarity = SelectField('Clarity', 
        choices=[('IF','IF'),('VVS1','VVS1'),('VVS2','VVS2'),('VS1','VS1'),('VS2','VS2'),('SI1','SI1'),('SI2','SI2'),('I1','I1')],
        validate_choice=True)
    x = DecimalField('X',
        validators=[validators.required(), validators.NumberRange(min=3.00, max=10)], default=5.73)
    y = DecimalField('Y',
        validators=[validators.required(), validators.NumberRange(min=3.00, max=10)], default=5.73)
    z = DecimalField('Z',
        validators=[validators.required(), validators.NumberRange(min=2.00, max=6)], default=3.53)
    
class PredictFeedbackForm(PredictForm):
    grade = SelectField('Grade', 
        choices=[('5','5'),('4','4'),('3','3'),('2','2'),('1','1')],
        validate_choice=True)

    user_prediction = StringField('User Prediction',
        validators=[validators.required(), 
        validators.Regexp('^(\d*\.?\d+|\d{1,3}(,\d{3})*(\.\d+)?)$', message="Not a valid number")])
    
    model_prediction = DecimalField('Model Prediction', 
        validators=[validators.required(), validators.NumberRange(min=0)])

class PredictView(FlaskView):

    @route('/', methods=['GET'])
    def index(self):
        response = requests.get(url=f"{fitservice}/fit/status")
        if response.status_code == 200:
            model_state = json.loads(response.text)
        
        if response.status_code != 200 or model_state['state'] != 'ready':
            return render_template('predict/not_ready.html')

        form = PredictForm(request.form)
        return render_template('predict/predict.html',state=model_state, form=form)
    
    @route('/', methods=['POST'])
    def submit_prediction(self):
        form = PredictForm(request.form)

        if form.validate():
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
            
            feedbackForm = PredictFeedbackForm(request.form)
            feedbackForm.user_prediction.data=""
            feedbackForm.model_prediction.data=float(response.text)
            return render_template('predict/predict_result.html',
                form=feedbackForm, row_id=int(audit_response.text))
         
        response = requests.get(url=f"{fitservice}/fit/status")
        model_state = json.loads(response.text)
        return render_template('predict/predict.html',state=model_state, form=form)


    @route('/feedback/<int:row_id>', methods=['POST','PUT'])
    def user_feedback(self, row_id):
        form = PredictFeedbackForm(request.form)
        if form.validate():
            grade = request.form['grade']
            user_prediction = request.form['user_prediction']
            data = {'grade':grade,'user_prediction':user_prediction}
            response = requests.put(url=f"{dataservice}/data/feedback/{row_id}", json=data)

            return render_template('predict/feedback_thank_you.html')
        
        form.user_prediction.data="" if form.user_prediction.data is None else form.user_prediction.data
        return render_template('predict/predict_result.html',
                form=form, row_id=int(row_id))



