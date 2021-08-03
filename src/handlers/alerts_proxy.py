from flask_classful import FlaskView, route
from flask import render_template, request
import pandas as pd
import os, requests, json

dataservice = os.environ['dataservice_endpoint']


class AlertsView(FlaskView):

    @route('/show_table/<string:table_name>', methods=['GET'])
    def show_table(self, table_name):
        limit = request.args.get('limit')
        order_by = request.args.get('order_by')
        order_asc_desc = request.args.get('order_asc_desc')
        response = requests.get(url=f"{dataservice}/data/table_view/{table_name}?limit={limit}&order_by={order_by}&order_asc_desc={order_asc_desc}")  
        data = json.loads(response.text)
        df = pd.read_json(data['df'])
        table_size = pd.read_json(data['size'])
        return render_template('alerts/alerts.html', data_table = df, size=table_size.iloc[0,0],
            table_name=table_name, limit=min(int(limit),table_size.iloc[0,0]),
             order_by=order_by, order_asc_desc=order_asc_desc)  
