from flask_classful import FlaskView, route
from flask import render_template, request
import requests, os
from wtforms import Form, validators, DecimalField, SelectField, StringField

fitservice = os.environ['fitservice_endpoint']
dataservice = os.environ['dataservice_endpoint']


class AdminActionsForm(Form):
    action_target = SelectField('Actions', 
        choices=[
            (f'{fitservice}/fit/train_model','Train Main Model'),
            (f'{fitservice}/fit/calc_score','Calculate Main Model Score'),
            (f'{dataservice}/data/load_new_data','Load New Data From Web'),
            (f'{fitservice}/fit/train_outsource_model','Train model using web data'),
            (f'{fitservice}/fit/calc_outsource_score','Calculate model score based on web data')
        ], validate_choice=True)

class AdminView(FlaskView):
      
    def index(self):
        form = AdminActionsForm(request.form)
        return render_template('admin/admin.html', form=form)
    
    @route('/action', methods=['POST'])
    def submit_action(self):
        form = AdminActionsForm(request.form)
        if form.validate():
            target = form.action_target.data
            requests.post(target)
            return render_template('admin/action_submitted.html')
        
        return render_template('admin/admin.html', form=form)
 

    
