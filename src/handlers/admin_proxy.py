from flask_classful import FlaskView, route
from flask import render_template, request
import requests, os

fitservice = os.environ['fitservice_endpoint']


class AdminView(FlaskView):
      
    def index(self):
        actions = (
            (f'{fitservice}/fit/train_model','Train Main Model'),
            (f'{fitservice}/fit/calc_score','Calculate Main Model Score')
        )
        return render_template('admin/admin.html', actions=actions)
    
    @route('/action', methods=['POST'])
    def submit_action(self):
        target = request.form['action_target']
        requests.post(target)
        return render_template('admin/action_submitted.html')



    

    
