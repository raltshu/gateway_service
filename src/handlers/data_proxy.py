import requests
import os
import pandas as pd
from flask_classful import FlaskView, route
from flask import request,render_template

dataservice = os.environ['dataservice_endpoint']

class DataView(FlaskView):

    @route('/', methods=['GET'])
    def index(self):
        response = requests.get(url=f"{dataservice}/data/table_view/diamonds_org?limit=10")
        df = pd.read_json(response.text)
        return render_template('data/data_show_table.html', data_table = df, table_name='diamonds_org', limit=10)

    @route('/show_table/<string:table_name>', methods=['GET'])
    def show_table(self, table_name):
        limit = request.args.get('limit')
        order_by = request.args.get('order_by')
        order_asc_desc = request.args.get('order_asc_desc')
        response = requests.get(url=f"{dataservice}/data/table_view/{table_name}?limit={limit}&order_by={order_by}&order_asc_desc={order_asc_desc}")  
        df = pd.read_json(response.text)
        return render_template('data/data_show_table.html', data_table = df, 
            table_name=table_name, limit=limit, order_by=order_by, order_asc_desc=order_asc_desc)  
    

