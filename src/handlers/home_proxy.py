import os
import requests
from flask_classful import FlaskView, route
from flask import request,render_template

dataservice = os.environ['dataservice_endpoint']

class HomeView(FlaskView):

    def index(self):
    
        return render_template('home/list.html')
    
    # @route('/predict', methods=['GET'])
    # def predict_view(self):
    #     return render_template('predict.html')

