import requests
import os
import pandas as pd
from flask_classful import FlaskView, route
from flask import request,render_template

dataservice = os.environ['dataservice_endpoint']

class DataView(FlaskView):

    @route('/', methods=['GET'])
    def index(self):
        #TODO: Data service get first 20 lines for display
        response = requests.get(url=f"{dataservice}/data/table_view/diamonds_org?limit=10")
        df = pd.read_json(response.text)
        return render_template('data/data_show_table.html', data_table = df, table_name='diamonds_org', limit=10)

    @route('/show_table/<string:table_name>', methods=['GET'])
    def show_table(self, table_name):
        limit = request.args.get('limit')
        response = requests.get(url=f"{dataservice}/data/table_view/{table_name}?limit={limit}")  
        df = pd.read_json(response.text)
        return render_template('data/data_show_table.html', data_table = df, table_name=table_name, limit=limit)  
    # @route('/', methods=['POST'])
    # def submit_prediction(self):
    #     return render_template('predict/predict.html')


